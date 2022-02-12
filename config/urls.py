from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth.models import Group
from django.conf.urls.static import static
from config.utils import SWAGGER_URLS
from config.admins.admin_config import AdminConfig
from config.admins.kairos_admin import kairos_admin_site

urlpatterns = [
    path("admin/", admin.site.urls),
    path("admins/kairos/", kairos_admin_site.urls),
    path("users/", include("dj_rest_auth.urls")),
    path("users/", include("users.urls")),
    path("posts/", include("posts.urls")),
    path("comments/", include("comments.urls")),
    path("mentors/", include("mentors.urls")),
]

# admin config
unregister_apps = [Group]
admin_config = AdminConfig(unregister_apps=unregister_apps)
admin_config.unregister_admin_apps()
admin_config.change_admin_values("카이로스 ADMIN", "카이로스 ADMIN", "카이로스 관리")

if settings.DEBUG:
    urlpatterns += (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + SWAGGER_URLS
    )
