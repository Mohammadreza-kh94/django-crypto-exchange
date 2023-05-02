from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from accounts.models import User
from crypto.models import Crypto
from purchase.models import Purchase
from wallet.models import Wallet


class PurchaseCryptoTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpass", wallet_balance=20.00
        )
        self.crypto = Crypto.objects.create(name="Aban", symbol="ABN", price=Decimal("4.00"))

    def test_purchase_crypto(self):
        self.client.force_login(self.user)
        url = reverse("purchase-crypto")
        data = {"crypto_id": self.crypto.id, "quantity": Decimal("3.00")}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(Wallet.objects.get(user_id=self.user.id, crypto_id=self.crypto.id).balance, Decimal("3.00"))
        self.assertEqual(Purchase.objects.count(), 1)

    def test_purchase_crypto_insufficient_balance(self):
        self.client.force_login(self.user)
        url = reverse("purchase-crypto")
        data = {"crypto_id": self.crypto.id, "quantity": Decimal("15.00")}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Payment declined. Insufficient balance.")

    def test_purchase_crypto_under_ten_dollars(self):
        self.client.force_login(self.user)
        url = reverse("purchase-crypto")
        data = {"crypto_id": self.crypto.id, "quantity": Decimal("1.00")}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertEqual(Purchase.objects.get(user_id=self.user.id, crypto_id=self.crypto.id).is_settled, False)

        self.user.refresh_from_db()
        self.assertEqual(self.user.wallet_balance, 16.00)

        queryset = Wallet.objects.filter(user_id=self.user.id, crypto_id=self.crypto.id)
        self.assertQuerysetEqual(queryset, [])
