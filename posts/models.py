from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from core.models import TimeStampModel


class KnowHowPost(TimeStampModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="knowhow_profile",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=100)
    cover = models.ImageField(
        blank=True, null=True, upload_to="knowhow/images/%Y/%m/%d"
    )
    content = models.TextField()
    like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="knowhow_like_set"
    )
    tags = TaggableManager(blank=True)


class Photo(TimeStampModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="photo", on_delete=models.CASCADE
    )
    description = models.CharField(max_length=255, default="")
    tags = TaggableManager(blank=True)
    like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="photo_like_set"
    )


class PhotoImage(models.Model):
    post = models.ForeignKey(
        Photo, on_delete=models.CASCADE, related_name="photo_image"
    )
    image = models.ImageField(blank=True, null=True, upload_to="photo/images/%Y/%m/%d")


class Video(TimeStampModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="video", on_delete=models.CASCADE
    )
    video = models.FileField(upload_to="video/videos/%Y/%m/%d")
    description = models.CharField(max_length=255, default="")
    tags = TaggableManager(blank=True)
    like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="video_like_set"
    )


class Bookmark(TimeStampModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="bookmark", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=20, default="나의 북마크")
    urls = models.URLField()
