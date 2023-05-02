from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from accounts.models import User
from crypto.models import Crypto

from .models import Wallet


class WalletViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com", username="testuser", password="testpass")
        self.crypto = Crypto.objects.create(name="Aban", symbol="ABN", price=4.00)
        self.wallet = Wallet.objects.create(user=self.user, crypto=self.crypto, balance=2.0)

    def test_get_wallet_detail(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        url = reverse("wallet")
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {"id": self.wallet.id, "user": self.user.id, "crypto": self.crypto.id, "balance": "2.00"}
        self.assertEqual(dict(response.data[0]), expected_data)
