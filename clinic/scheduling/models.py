from django.db import models

class Booking(models.Model):
    APPT_CHOICES = [(k, k.title()) for k in ["consultation","follow-up","physical","telehealth"]]

    date = models.DateField()
    time = models.TimeField()
    appt_type = models.CharField(max_length=32, choices=APPT_CHOICES)
    patient_name = models.CharField(max_length=255)
    patient_phone = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("date", "time")
