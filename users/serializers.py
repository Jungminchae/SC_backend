from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import Profile


class UserSerializer(RegisterSerializer):
    pass


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ("id", "user", "name", "avatar", "bio", "followers", "followings")
        read_only_fields = ("id", "followers", "followings")
