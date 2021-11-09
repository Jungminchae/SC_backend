from django.db import models
from core.models import TimeStampModel


class KnowHowPost(TimeStampModel):
    user = models.ForeignKey(
        "users.Profile", related_name="knowhow_profile", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    like = models.ManyToManyField("users.Profile", related_name="like")


class KnowHowPostImage(models.Model):
    post = models.ForeignKey(
        KnowHowPost, on_delete=models.CASCADE, related_name="knowhow_image"
    )
    image = models.ImageField(
        blank=True, null=True, upload_to="knowhow/images/%Y/%m/%d"
    )


class Photo(TimeStampModel):
    user = models.ManyToManyField("users.Profile", related_name="photo")
    photo = models.ImageField(upload_to="photo/images/%Y/%m/%d")
    description = models.CharField(max_length=255, default="")


class Video(TimeStampModel):
    user = models.ManyToManyField("users.Profile", related_name="video")
    video = models.FileField(upload_to="video/videos/%Y/%m/%d")
    description = models.CharField(max_length=255, default="")


class Bookmark(TimeStampModel):
    user = models.ManyToManyField("users.Profile", related_name="bookmark")
    name = models.CharField(max_length=20, default="나의 북마크")
    urls = models.URLField()
