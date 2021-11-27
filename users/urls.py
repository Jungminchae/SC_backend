from django.urls import path
from .views import google_login, google_callback, GoogleLogin, SignupView

urlpatterns = [
    path("registration/email", SignupView.as_view(), name="sign-up-email"),
    path("google/login/", google_login, name="google_login"),
    path("google/callback/", google_callback, name="google_callback"),
    path(
        "google/login/finish/",
        GoogleLogin.as_view(),
        name="google_login_todjango",
    ),
]
