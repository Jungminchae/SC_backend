from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from core.models import TimeStampModel


class KnowHowPost(TimeStampModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="knowhow_profile",
        on_delete=models.PROTECT,
        verbose_name=_("회원"),
    )
    title = models.CharField(max_length=100, verbose_name=_("제목"))
    cover = models.ImageField(
        blank=True,
        null=True,
        upload_to="knowhow/images/%Y/%m/%d",
        verbose_name=_("커버사진"),
    )
    content = models.TextField(verbose_name=_("내용"))
    like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="knowhow_like_set",
        verbose_name=_("좋아요"),
    )
    tags = TaggableManager(blank=True, verbose_name=_("태그"))
    only_me = models.BooleanField(blank=True, default=False, verbose_name=_("나만보기"))

    class Meta:
        verbose_name = _("노하우")
        verbose_name_plural = _("노하우 게시판 관리")

    def __str__(self):
        return self.title


class Photo(TimeStampModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="photo",
        on_delete=models.PROTECT,
        verbose_name=_("회원"),
    )
    title = models.CharField(max_length=100, verbose_name=_("제목"))
    description = models.CharField(max_length=255, default="", verbose_name=_("내용"))
    tags = TaggableManager(blank=True, verbose_name=_("태그"))
    like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="photo_like_set",
        verbose_name=_("좋아요"),
    )
    only_me = models.BooleanField(blank=True, default=False, verbose_name=_("나만보기"))

    class Meta:
        verbose_name = _("사진")
        verbose_name_plural = _("사진 관리")

    def __str__(self):
        return self.title


class PhotoImage(models.Model):
    post = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE,
        related_name="photo_image",
        verbose_name=_("포스트"),
    )
    image = models.ImageField(
        blank=True, null=True, upload_to="photo/images/%Y/%m/%d", verbose_name=_("사진")
    )

    class Meta:
        verbose_name = _("사진 파일")
        verbose_name_plural = _("사진 파일 관리")


class Video(TimeStampModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="video",
        on_delete=models.PROTECT,
        verbose_name=_("회원"),
    )
    title = models.CharField(max_length=100, verbose_name=_("제목"))
    video = models.FileField(upload_to="video/videos/%Y/%m/%d", verbose_name=_("비디오"))
    description = models.CharField(max_length=255, default="", verbose_name=_("내용"))
    tags = TaggableManager(blank=True, verbose_name=_("태그"))
    like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="video_like_set",
        verbose_name=_("좋아요"),
    )
    only_me = models.BooleanField(blank=True, default=False, verbose_name=_("나만보기"))

    class Meta:
        verbose_name = _("동영상")
        verbose_name_plural = _("동영상 관리")

    def __str__(self):
        return self.title


class Bookmark(TimeStampModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="bookmark",
        on_delete=models.CASCADE,
        verbose_name=_("회원"),
    )
    name = models.CharField(max_length=20, default="나의 북마크", verbose_name=_("북마크"))
    urls = models.URLField(verbose_name=_("링크"))

    def __str__(self):
        return self.name
