from rest_framework import serializers
from .models import KnowHowComment, PhotoComment, VideoComment
from users.serializers import ProfileSerializer


class KnowHowCommentSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    reply = serializers.SerializerMethodField()

    class Meta:
        model = KnowHowComment
        fields = ("id", "profile", "post", "comment", "created_at", "updated_at", "reply")
        read_only_fields = ("id", "created_at", "updated_at")

    def get_reply(self, instance):
        serializer = self.__class__(instance.replies, many=True)
        serializer.bind("", self)
        return serializer.data

class PhotoCommentSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    reply = serializers.SerializerMethodField()

    class Meta:
        model = PhotoComment
        fields = ("id", "profile", "comment", "created_at", "updated_at", "reply")
        read_only_fields = ("id", "created_at", "updated_at")

    def get_reply(self, instance):
        serializer = self.__class__(instance.replies, many=True)
        serializer.bind("", self)
        return serializer.data

class VideoCommentSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    reply = serializers.SerializerMethodField()

    class Meta:
        model = VideoComment
        fields = ("id", "profile", "comment", "created_at", "updated_at", "reply")
        read_only_fields = ("id", "created_at", "updated_at")
        
    def get_reply(self, instance):
        serializer = self.__class__(instance.replies, many=True)
        serializer.bind("", self)
        return serializer.data