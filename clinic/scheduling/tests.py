from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

class SchedulingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_availability_and_booking_flow(self):
        date = "2025-01-10"
        # check availability
        resp = self.client.get(reverse('calendly-availability'), {'date': date, 'type':'consultation'})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('available_slots', data)
        slot = data['available_slots'][0]

        # book that slot
        book_resp = self.client.post(reverse('calendly-book'), {
            'date': date, 'time': slot, 'type': 'consultation',
            'patient': {'name':'Alice','phone':'1112223333'}
        }, format='json')
        self.assertEqual(book_resp.status_code, 201)

        # second booking attempt same slot should fail
        book_resp2 = self.client.post(reverse('calendly-book'), {
            'date': date, 'time': slot, 'type': 'consultation',
            'patient': {'name':'Bob','phone':'4445556666'}
        }, format='json')
        self.assertEqual(book_resp2.status_code, 400)
