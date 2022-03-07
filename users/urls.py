from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    SignupView,
    ProfileViewSet,
    toggle_follow,
)

router = DefaultRouter()
router.register("profiles", ProfileViewSet)

urlpatterns = [
    path("registration/email/", SignupView.as_view(), name="sign-up-email"),
    path("follows/", toggle_follow, name="toggle-follow"),
] + router.urls
