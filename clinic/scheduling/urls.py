from django.urls import path
from . import views

urlpatterns = [
    path('calendly/availability', views.GetAvailability, name='calendly-availability'),
    path('calendly/book', views.BookAppointment, name='calendly-book'),
]
