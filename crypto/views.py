from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Crypto
from .serializers import CryptoSerializer


class CryptoListAPIView(generics.ListAPIView):
    queryset = Crypto.objects.all()
    serializer_class = CryptoSerializer
    permission_classes = [AllowAny]


class CryptoDetailAPIView(generics.RetrieveAPIView):
    queryset = Crypto.objects.all()
    serializer_class = CryptoSerializer
    permission_classes = [AllowAny]
