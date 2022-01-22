from django.urls import path
from mentors.views import MentorView


urlpatterns = [path("", MentorView.as_view(), name="mentor")]
