from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wallet
from .serializers import WalletSerializer


class WalletDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        wallet = Wallet.objects.filter(user=user)
        serializer = WalletSerializer(wallet, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
