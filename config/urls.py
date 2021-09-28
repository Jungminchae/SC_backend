from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auths/", include("dj_rest_auth.urls")),
    path("auths/", include("auths.urls")),
    path("auths/", include("allauth.urls")),
    path("users/", include("users.urls")),
]
