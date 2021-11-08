from django.db import models
from core.models import TimeStampModel


class Post(TimeStampModel):
    user = models.ForeignKey(
        "accounts.Profile", related_name="post_profile", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    like = models.ManyToManyField("accounts.Profile", related_name="like")


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_image")
    image = models.ImageField(blank=True, null=True, upload_to="posts/images/%Y/%m/%d")


class Bookmark(TimeStampModel):
    user = models.ManyToManyField("accounts.Profile", related_name="bookmark")
    name = models.CharField(default="나의 북마크")
    urls = models.URLField()
