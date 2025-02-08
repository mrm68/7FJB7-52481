from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Reservation, Table
from accounts.models import CustomUser

class ReservationURLTests(APITestCase):
    def setUp(self):
        # Create a user and log in
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create a table
        self.table = Table.objects.create(seats=6, available=True)

        # Create a reservation
        self.reservation = Reservation.objects.create(
            user=self.user,
            table=self.table,
            date="2023-10-15",
            time="18:00",
            guests=4
        )

    def test_reservation_list_url(self):
        # Get the URL for the reservation list
        url = reverse('reservationList')

        # Make a GET request to the reservation list URL
        response = self.client.get(url)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Optionally, check that the response contains the reservation we created
        self.assertEqual(len(response.data), 1)  # Assuming the response is a list of reservations
        self.assertEqual(response.data[0]['id'], self.reservation.id)

    def test_reservation_detail_url(self):
        # Get the URL for the reservation detail view
        url = reverse('reservationDetail', args=[self.reservation.id])

        # Make a GET request to the reservation detail URL
        response = self.client.get(url)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains the correct reservation data
        self.assertEqual(response.data['id'], self.reservation.id)
        self.assertEqual(response.data['table'], self.table.id)
        self.assertEqual(response.data['date'], "2023-10-15")
        self.assertEqual(response.data['time'], "18:00")
        self.assertEqual(response.data['guests'], 4)