from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("", include("crypto.urls")),
    path("", include("wallet.urls")),
    path("", include("purchase.urls")),
]
