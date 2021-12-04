from django.db import models
from django.conf import settings
from core.models import TimeStampModel


# TODO: 멘토 항목은 정해지면 개발
class Mentor(TimeStampModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mentor"
    )
