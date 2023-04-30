from django.urls import path

from .views import charge_wallet, login, register

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("charge_wallet/", charge_wallet, name="charge_wallet"),
]
