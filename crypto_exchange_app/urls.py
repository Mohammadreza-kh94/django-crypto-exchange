from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Crypto Exchange API",
        default_version="v1",
        description="API documentation for the Crypto Exchange application",
        contact=openapi.Contact(email="f69.khoobbakht@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("", include("crypto.urls")),
    path("", include("wallet.urls")),
    path("", include("purchase.urls")),
    re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
