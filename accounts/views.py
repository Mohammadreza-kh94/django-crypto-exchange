from decimal import Decimal

from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        response = {"message": "User Created Successfully", "token": token.key}
        return Response({"token": response}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user:
        user.last_login = timezone.now()
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
    else:
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def charge_wallet(request):
    user = request.user
    amount = request.data.get("amount")

    if not amount:
        return Response({"error": "Please provide an amount to charge."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user.wallet_balance += Decimal(amount)
        user.save()
        return Response({"message": f"Wallet successfully charged with {amount}."}, status=status.HTTP_200_OK)
    except ValueError:
        return Response({"error": "Please provide a valid amount."}, status=status.HTTP_400_BAD_REQUEST)
