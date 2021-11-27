from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import Profile


class UserSerializer(RegisterSerializer):
    pass


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
