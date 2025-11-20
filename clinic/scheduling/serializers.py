from rest_framework import serializers
from .models import Booking

class PatientSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=50, required=False, allow_blank=True)

class BookingSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(write_only=True)

    class Meta:
        model = Booking
        fields = ('id','date','time','appt_type','patient','created_at')
        read_only_fields = ('id','created_at')

    def create(self, validated_data):
        patient = validated_data.pop('patient')
        booking = Booking.objects.create(
            patient_name = patient.get('name'),
            patient_phone = patient.get('phone'),
            **validated_data
        )
        return booking
