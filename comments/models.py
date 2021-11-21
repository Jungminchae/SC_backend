from django.db import models
from django.conf import settings
from core.models import TimeStampModel


class KnowHowComment(TimeStampModel):
    post = models.ForeignKey(
        "posts.KnowHowPost", related_name="comments", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="knowhow_comments",
        on_delete=models.CASCADE,
    )
    comment = models.CharField(max_length=255)


class PhotoComment(TimeStampModel):
    post = models.ForeignKey(
        "posts.Photo", related_name="comments", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="photo_comments",
        on_delete=models.CASCADE,
    )
    comment = models.CharField(max_length=255)


class VideoComment(TimeStampModel):
    post = models.ForeignKey(
        "posts.Video", related_name="comments", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="video_comments",
        on_delete=models.CASCADE,
    )
    comment = models.CharField(max_length=255)
