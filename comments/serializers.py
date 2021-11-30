from rest_framework import serializers
from .models import KnowHowComment, PhotoComment, VideoComment
from users.serializers import ProfileSerializer


class KnowHowCommentSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = KnowHowComment
        fields = ("id", "profile", "comment", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class PhotoCommentSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = PhotoComment
        fields = ("id", "profile", "comment", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class VideoCommentSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = VideoComment
        fields = ("id", "profile", "comment", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
