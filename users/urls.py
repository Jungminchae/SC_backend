from django.urls import path
from .views import google_login, google_callback, GoogleLogin

urlpatterns = [
    path("google/login/", google_login, name="google_login"),
    path("google/callback/", google_callback, name="google_callback"),
    path(
        "users/google/login/finish/",
        GoogleLogin.as_view(),
        name="google_login_todjango",
    ),
]
