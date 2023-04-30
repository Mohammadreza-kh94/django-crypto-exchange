from django.urls import path

from .views import WalletDetailView

urlpatterns = [
    path("wallet/", WalletDetailView.as_view(), name="wallet"),
]
