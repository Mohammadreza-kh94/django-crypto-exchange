from django.urls import path

from .views import PurchaseCryptoView, PurchaseHistoryAPIView

urlpatterns = [
    path("purchase/", PurchaseCryptoView.as_view(), name="purchase-crypto"),
    path("purchase-history/", PurchaseHistoryAPIView.as_view(), name="purchase-history"),
]
