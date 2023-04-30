from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Crypto
from .serializers import CryptoSerializer


class CryptoListAPIView(generics.ListAPIView):
    queryset = Crypto.objects.all()
    serializer_class = CryptoSerializer
    permission_classes = [IsAuthenticated]


class CryptoDetailAPIView(generics.RetrieveAPIView):
    queryset = Crypto.objects.all()
    serializer_class = CryptoSerializer
    permission_classes = [IsAuthenticated]
