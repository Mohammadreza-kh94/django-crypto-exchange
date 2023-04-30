from rest_framework import serializers

from crypto.serializers import CryptoSerializer

from .models import Purchase


class PurchaseSerializer(serializers.ModelSerializer):
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Purchase
        fields = [
            "user",
            "crypto",
            "quantity",
            "total_price",
            "is_settled",
        ]
