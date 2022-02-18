from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin
from core.permissions import IsMe
from core.utils import like_or_unlike
from posts.models import KnowHowPost, Photo, Video
from users.models import Profile
from comments.models import KnowHowComment, PhotoComment, VideoComment
from comments.serializers import (
    KnowHowCommentSerializer,
    PhotoCommentSerializer,
    VideoCommentSerializer,
)



class KnowHowCommentViewSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = KnowHowComment.objects.all()
    serializer_class = KnowHowCommentSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsMe]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(post__id=self.kwargs["post_id"])
        return queryset

    def perform_create(self, serializer):
        profile = get_object_or_404(Profile, user=self.request.user)
        post = get_object_or_404(KnowHowPost, id=self.kwargs["post_id"])
        serializer.save(user=self.request.user, post=post, profile=profile)
        return super().perform_create(serializer)

    @action(detail=True, methods=["POST", "DELETE"], url_path="likes")
    def like_knowhow_comment(self, request, post_id, pk):
        user = request.user
        response = like_or_unlike(KnowHowComment, user, pk)
        return response


class PhotoCommentViewSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = PhotoComment.objects.all()
    serializer_class = PhotoCommentSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsMe]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(post__id=self.kwargs["post_id"])
        return queryset

    def perform_create(self, serializer):
        profile = get_object_or_404(Profile, user=self.request.user)
        post = get_object_or_404(Photo, id=self.kwargs["post_id"])
        serializer.save(user=self.request.user, post=post, profile=profile)
        return super().perform_create(serializer)

    @action(detail=True, methods=["POST", "DELETE"], url_path="likes")
    def like_photo_comment(self, request, pk):
        user = request.user
        response = like_or_unlike(PhotoComment, user, pk)
        return response


class VideoCommentViewSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = VideoComment.objects.all()
    serializer_class = VideoCommentSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsMe]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(post__id=self.kwargs["post_id"])
        return queryset

    def perform_create(self, serializer):
        profile = get_object_or_404(Profile, user=self.request.user)
        post = get_object_or_404(Video, id=self.kwargs["post_id"])
        serializer.save(user=self.request.user, post=post, profile=profile)
        return super().perform_create(serializer)
    
    @action(detail=True, methods=["POST", "DELETE"], url_path="likes")
    def like_video_comment(self, request, post_id, pk):
        user = request.user
        response = like_or_unlike(VideoComment, user, pk)
        return response

