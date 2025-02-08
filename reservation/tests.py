from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient, force_authenticate
from rest_framework import status
from .models import Table, Reservation

class ReservationDetailTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret",
        )
        cls.other_user = get_user_model().objects.create_user(
            username="otheruser",
            email="other@email.com",
            password="secret",
        )
        cls.table = Table.objects.create(seats=6, available=True)
        cls.reservation = Reservation.objects.create(
            user=cls.user,
            table=cls.table,
            seats_reserved=4,
            cost=300,
        )
        cls.other_reservation = Reservation.objects.create(
            user=cls.other_user,
            table=cls.table,
            seats_reserved=4,
            cost=300,
        )
    
    def setUp(self):
        self.client = APIClient()
    
    # RETRIEVE OWN
    def test_retrieve_own_reservation_detail(self):
        """Test retrieving own reservation detail"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/reservations/{self.reservation.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['seats_reserved'], 4)
        self.assertEqual(response.data['cost'], 300)
    
    # FORBIDDEN OTHER
    def test_retrieve_other_user_reservation_detail(self):
        """Test retrieving another user's reservation detail, should be not found or forbidden"""
        # did I really have to force authenticate ?
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/reservations/{self.other_reservation.id}/')
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])
    
    # DELETE OWN
    def test_delete_own_reservation(self):
        """Test deleting own reservation"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/reservations/{self.reservation.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Reservation.objects.filter(id=self.reservation.id).count(), 0)
    
    # DELETE OTHER
    def test_delete_other_user_reservation(self):
        """Test deleting another user's reservation, should be not found or forbidden"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/reservations/{self.other_reservation.id}/')
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])
    
    # UNAUTH RETRIEVE
    def test_unauthenticated_user_cannot_retrieve_reservation_detail(self):
        """Test unauthenticated user cannot retrieve reservation detail"""
        response = self.client.get(f'/api/reservations/{self.reservation.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    # UNAUTH DELETE
    def test_unauthenticated_user_cannot_delete_reservation(self):
        """Test unauthenticated user cannot delete reservation"""
        response = self.client.delete(f'/api/reservations/{self.reservation.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
