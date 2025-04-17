from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import Order

User = get_user_model()

class OrderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            password='testpass123'
        )
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
        self.order1 = Order.objects.create(
            user=self.user,
            status='PENDING',
            total=100.00,
            items={'item1': {'name': 'Pizza', 'price': 100.00, 'quantity': 1}}
        )
        self.order2 = Order.objects.create(
            user=self.user,
            status='COMPLETED',
            total=200.00,
            items={'item1': {'name': 'Burger', 'price': 50.00, 'quantity': 4}}
        )
        self.client = APIClient()

    def test_get_all_orders_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_all_orders_unauthenticated(self):
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_orders_by_status(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('order-list') + '?status=completed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'COMPLETED')

    def test_cancel_order(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('order-cancel', kwargs={'pk': self.order1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order1.refresh_from_db()
        self.assertEqual(self.order1.status, 'CANCELLED')

    def test_cancel_completed_order_fails(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('order-cancel', kwargs={'pk': self.order2.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_admin_update_status(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('order-update-status', kwargs={'pk': self.order1.id})
        response = self.client.patch(url, {'status': 'PROCESSING'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order1.refresh_from_db()
        self.assertEqual(self.order1.status, 'PROCESSING')

    def test_non_admin_cannot_update_status(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('order-update-status', kwargs={'pk': self.order1.id})
        response = self.client.patch(url, {'status': 'PROCESSING'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
