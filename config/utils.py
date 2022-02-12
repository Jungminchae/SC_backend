from django.urls import path
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# swagger
schema_view = get_schema_view(
    openapi.Info(
        title="카이로스 API",
        default_version="v1",
        description="API for 카이로스",
        terms_of_service="https://www.카이로스.com/policies/terms/",
        contact=openapi.Contact(email="minchae3616@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

SWAGGER_URLS = [
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
