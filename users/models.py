from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import TimeStampModel
from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=255)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=50)
    avatar = models.ImageField(
        blank=True,
        upload_to="users/avatar/%Y/%m/%d",
        help_text="png/jpg 파일을 업로드해주세요.",
    )
    bio = models.TextField(blank=True)
    followers = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="following"
    )
    followings = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="follwer"
    )

    def like_counts(self):
        return self.like.count()
