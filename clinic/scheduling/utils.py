from datetime import datetime, timedelta, time as dt_time
from typing import List

# Appointment types and durations (minutes)
APPOINTMENT_TYPES = {
    "consultation": 30,
    "follow-up": 15,
    "physical": 45,
    "telehealth": 20,
}

# Example clinic working hours (start, end) — can be made per-day
CLINIC_START = dt_time(hour=9, minute=0)   # 09:00
CLINIC_END   = dt_time(hour=17, minute=0)  # 17:00

def parse_date(date_str: str) -> datetime.date:
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def generate_slots_for_date(date_obj, duration_minutes:int) -> List[str]:
    slots = []
    start_dt = datetime.combine(date_obj, CLINIC_START)
    end_dt   = datetime.combine(date_obj, CLINIC_END)
    current = start_dt
    delta = timedelta(minutes=duration_minutes)
    while current + delta <= end_dt:
        slots.append(current.strftime("%H:%M"))
        current += delta
    return slots
