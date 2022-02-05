from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
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
    profile = models.ForeignKey(
        "users.Profile", related_name="comments", on_delete=models.CASCADE
    )
    comment = models.CharField(max_length=255)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("노하우 게시판 댓글")
        verbose_name_plural = _("노하우 게시판 댓글 관리")

    def __str__(self):
        return f"{self.post.id}번글의 댓글: {self.comment}"


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

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("사진 게시판 댓글")
        verbose_name_plural = _("사진 게시판 댓글 관리")

    def __str__(self):
        return f"{self.post.id}번글의 댓글: {self.comment}"


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

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("동영상 게시판 댓글")
        verbose_name_plural = _("동영상 게시판 댓글 관리")

    def __str__(self):
        return f"{self.post.id}번글의 댓글: {self.comment}"
