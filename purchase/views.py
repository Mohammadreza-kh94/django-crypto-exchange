from decimal import Decimal

from django.db import transaction
from django.db.models import Sum
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from crypto.models import Crypto
from wallet.models import Wallet

from .models import Purchase
from .serializers import PurchaseSerializer
from .utils import buy_from_exchange


class PurchaseCryptoView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, format=None):
        crypto_id = request.data.get("crypto_id")
        quantity = request.data.get("quantity")

        if not crypto_id or not quantity:
            return Response({"error": "crypto_id and quantity are required"}, status=status.HTTP_400_BAD_REQUEST)

        if quantity < 1:
            return Response({"error": "Amount must be positive."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            crypto = Crypto.objects.get(id=crypto_id)
        except Crypto.DoesNotExist:
            return Response({"error": "invalid crypto_id"}, status=status.HTTP_400_BAD_REQUEST)

        total_cost = crypto.price * Decimal(quantity)

        if request.user.wallet_balance < total_cost:
            return Response({"error": "Payment declined. Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)

        # convert update user row in a seprate function
        user_account = User.objects.select_for_update().get(username=request.user)
        user_account.wallet_balance -= total_cost
        user_account.save()

        purchase = Purchase.objects.create(
            user=request.user,
            crypto=crypto,
            quantity=quantity,
            total_price=total_cost,
        )

        not_settled_purchases = Purchase.objects.filter(crypto_id=crypto_id, is_settled=False)
        total_price_sum = not_settled_purchases.aggregate(Sum("total_price"))["total_price__sum"]

        if total_price_sum > 10:
            total_amount = not_settled_purchases.aggregate(Sum("quantity"))["quantity__sum"]
            buy_from_exchange(crypto_id=crypto_id, crypto_amount=total_amount)

            for item in not_settled_purchases:
                update_user_wallet(user_id=item.user_id, crypto_id=item.crypto_id, quantity=item.quantity)

            not_settled_purchases.update(is_settled=True)

        # if total_cost < 10:
        #     return settle_small_order(request.user, crypto_id, quantity)

        # if check_all_settled(crypto_name):
        #     buy_from_exchange(crypto_name, total_price)

        # serializer = PurchaseSerializer(purchase)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"success": True, "order_id": purchase.id})


class PurchaseHistoryAPIView(ListAPIView):
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Purchase.objects.filter(user=self.request.user)


@transaction.atomic
def update_user_wallet(user_id, crypto_id, quantity):
    wallet, created = Wallet.objects.get_or_create(user_id=user_id, crypto_id=crypto_id)

    if created:
        wallet.balance = Decimal(quantity)
    else:
        wallet.balance += Decimal(quantity)
    wallet.save()
