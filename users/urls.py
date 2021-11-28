from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    google_login,
    google_callback,
    GoogleLogin,
    SignupView,
    ProfileViewSet,
    toggle_follow,
)

router = DefaultRouter()
router.register("profiles", ProfileViewSet)

urlpatterns = [
    path("registration/email/", SignupView.as_view(), name="sign-up-email"),
    path("google/login/", google_login, name="google_login"),
    path("google/callback/", google_callback, name="google_callback"),
    path(
        "google/login/finish/",
        GoogleLogin.as_view(),
        name="google_login_todjango",
    ),
    path("follows/", toggle_follow, name="toggle-follow"),
] + router.urls
