from rest_framework import serializers
from .models import KnowHowComment, PhotoComment, VideoComment


class KnowHowCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowHowComment
        fields = ("id", "user", "post", "comment", "created_at", "updated_at")
        read_only_fields = ("id", "user", "created_at", "updated_at")


class PhotoCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoComment
        fields = ("id", "user", "post", "comment", "created_at", "updated_at")
        read_only_fields = ("id", "user", "created_at", "updated_at")


class VideoCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoComment
        fields = ("id", "user", "post", "comment", "created_at", "updated_at")
        read_only_fields = ("id", "user", "created_at", "updated_at")
