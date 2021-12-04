from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django_pydenticon.views import image as pydenticon_image
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

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


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("dj_rest_auth.urls")),
    path("users/", include("users.urls")),
    path("identicons/image/<path:data>/", pydenticon_image, name="pydenticon_image"),
    path("posts/", include("posts.urls")),
    path("comments/", include("comments.urls")),
    path("mentors/", include("mentors.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
        path(
            "",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
        ),
    ]
