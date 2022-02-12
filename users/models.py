from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampModel
from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=255, verbose_name=_("이메일"))

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("가입회원 목록")
        verbose_name_plural = _("가입회원 목록")


class Profile(TimeStampModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="profile", verbose_name=_("회원")
    )
    name = models.CharField(max_length=50, verbose_name=_("이름"))
    avatar = models.ImageField(
        blank=True,
        upload_to="users/avatar/%Y/%m/%d",
        help_text="png/jpg 파일을 업로드해주세요.",
        verbose_name=_("프로필 사진"),
    )
    bio = models.TextField(blank=True, verbose_name=_("소개"))
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="following",
        verbose_name=_("팔로워"),
    )
    followings = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="follwer",
        verbose_name=_("팔로잉"),
    )

    def like_counts(self):
        return self.like.count()

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = _("회원 프로필 목록")
        verbose_name_plural = _("회원 프로필 목록")
