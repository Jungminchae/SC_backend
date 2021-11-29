from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from core.permissions import IsMe
from posts.models import KnowHowPost, Photo, Video
from .models import KnowHowComment, PhotoComment, VideoComment
from .serializers import (
    KnowHowCommentSerializer,
    PhotoCommentSerializer,
    VideoCommentSerializer,
)


class KnowHowCommentViewSet(ModelViewSet):
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
        post = get_object_or_404(KnowHowPost, id=self.kwargs["post_id"])
        serializer.save(user=self.request.user, post=post)
        return super().perform_create(serializer)


class PhotoCommentViewSet(ModelViewSet):
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
        post = get_object_or_404(Photo, id=self.kwargs["post_id"])
        serializer.save(user=self.request.user, post=post)
        return super().perform_create(serializer)


class VideoCommentViewSet(ModelViewSet):
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
        post = get_object_or_404(Video, id=self.kwargs["post_id"])
        serializer.save(user=self.request.user, post=post)
        return super().perform_create(serializer)
