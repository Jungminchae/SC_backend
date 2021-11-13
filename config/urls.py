from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django_pydenticon.views import image as pydenticon_image

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("dj_rest_auth.urls")),
    path("users/", include("allauth.urls")),
    path("users/", include("users.urls")),
    path("identicons/image/<path:data>/", pydenticon_image, name="pydenticon_image"),
    path("posts/", include("posts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
