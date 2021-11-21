from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from core.permissions import IsMe
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PhotoCommentViewSet(ModelViewSet):
    queryset = PhotoComment.objects.all()
    serializer_class = PhotoCommentSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsMe]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VideoCommentViewSet(ModelViewSet):
    queryset = VideoComment.objects.all()
    serializer_class = VideoCommentSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsMe]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
