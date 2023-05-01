from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User


class RegisterTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register")
        self.user_data = {"email": "test@test.com", "username": "testuser", "password": "testpassword"}

    def test_registration(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("login")
        self.login_data = {"username": "testuser", "password": "testpassword"}
        self.user = User.objects.create_user(email="test@test.com", username="testuser", password="testpassword")

    def test_login(self):
        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ChargeWalletTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.charge_wallet_url = reverse("charge_wallet")
        self.user = User.objects.create_user(email="test@test.com", username="testuser", password="testpassword")

    def test_charge_wallet_balance(self):
        self.client.force_login(self.user)

        response = self.client.post(self.charge_wallet_url, {"amount": 500})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.wallet_balance, Decimal("500"))
