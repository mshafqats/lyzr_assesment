from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, time as dt_time
from .utils import APPOINTMENT_TYPES, parse_date, generate_slots_for_date
from .models import Booking
from .serializers import BookingSerializer

@api_view(['GET'])
def GetAvailability(request):
    """
        GET params:
            - date=YYYY-MM-DD (required)
            - type=<appointment_type> (optional; default consultation)
        Response example:
        {
            "date": "2025-01-10",
            "type": "consultation",
            "available_slots": ["09:00", "09:30", ...],
        }
    """
    date_str = request.GET.get('date')
    appt_type = request.GET.get('type', 'consultation').lower()

    if not date_str:
        return Response({"error": "Missing 'date' parameter (YYYY-MM-DD)"}, status=status.HTTP_400_BAD_REQUEST)

    if appt_type not in APPOINTMENT_TYPES:
        return Response({"error": f"Invalid appointment type. Valid: {list(APPOINTMENT_TYPES.keys())}"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        date_obj = parse_date(date_str)
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    duration = APPOINTMENT_TYPES[appt_type]
    all_slots = generate_slots_for_date(date_obj, duration)
    booked = Booking.objects.filter(date=date_obj).values_list('time', flat=True)
    booked_strs = {t.strftime("%H:%M") for t in booked}
    available = [s for s in all_slots if s not in booked_strs]

    if not available:
        return Response({ "date": date_str, "type": appt_type, "message": "No available slots", "available_slots": [] })

    return Response({ "date": date_str, "type": appt_type, "available_slots": available })


@api_view(['POST'])
def BookAppointment(request):
    """
        POST body:
        {
            "date": "2025-01-10",
            "time": "10:00",
            "type": "consultation",
            "patient": { "name": "John Doe", "phone": "9876..." }
        }
    """
    data = request.data
    date_str = data.get('date')
    time_str = data.get('time')
    appt_type = data.get('type', 'consultation').lower()
    patient = data.get('patient')

    if not (date_str and time_str and patient and isinstance(patient, dict)):
        return Response({"error": "Missing required fields: date, time, patient"}, status=status.HTTP_400_BAD_REQUEST)

    if appt_type not in APPOINTMENT_TYPES:
        return Response({"error": f"Invalid appointment type. Valid: {list(APPOINTMENT_TYPES.keys())}"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        date_obj = parse_date(date_str)
        time_obj = datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        return Response({"error": "Invalid date/time format. Date: YYYY-MM-DD, Time: HH:MM"}, status=status.HTTP_400_BAD_REQUEST)

    duration = APPOINTMENT_TYPES[appt_type]
    all_slots = generate_slots_for_date(date_obj, duration)
    if time_str not in all_slots:
        return Response({"error": "Requested time is outside clinic hours or invalid for this appointment type."}, status=status.HTTP_400_BAD_REQUEST)

    conflict = Booking.objects.filter(date=date_obj, time=time_obj).exists()
    if conflict:
        return Response({"error": "Slot already booked"}, status=status.HTTP_400_BAD_REQUEST)

    # Create booking
    payload = {
        "date": date_obj,
        "time": time_obj,
        "appt_type": appt_type,
        "patient": patient
    }

    serializer = BookingSerializer(data=payload)
    if serializer.is_valid():
        booking = serializer.save()
        return Response(
            {
                "message": "Booking confirmed",
                "booking": {
                    "id": booking.id,
                    "date": booking.date.isoformat(),
                    "time": booking.time.strftime("%H:%M"),
                    "type": booking.appt_type,
                    "patient": {
                        "name": booking.patient_name,
                        "phone": booking.patient_phone
                    }
                }
            },
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
