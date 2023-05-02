from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Crypto
from .serializers import CryptoSerializer


class CryptoTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.crypto1 = Crypto.objects.create(
            name="Bitcoin",
            symbol="BTC",
            price=50000.00,
        )

        self.crypto2 = Crypto.objects.create(
            name="Ethereum",
            symbol="ETH",
            price=3000.00,
        )

        self.crypto3 = Crypto.objects.create(
            name="Aban",
            symbol="ABN",
            price=4.00,
        )

        self.crypto4 = Crypto.objects.create(
            name="Tether",
            symbol="₮",
            price=1.00,
        )

    def test_crypto_list(self):
        url = reverse("crypto-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        serialize_data = CryptoSerializer([self.crypto1, self.crypto2, self.crypto3, self.crypto4], many=True).data
        self.assertEqual(response.data, serialize_data)

    def test_crypto_detail(self):
        url = reverse("crypto-detail", args=[self.crypto1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialized_data = CryptoSerializer(self.crypto1).data
        self.assertEqual(response.data, serialized_data)

    def test_crypto_does_not_exist(self):
        url = reverse("crypto-detail", args=[20])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Not found.")
