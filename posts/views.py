from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import status
from .models import KnowHowPost, Photo, Video, Bookmark
from .serializers import (
    KnowHowPostSerializer,
    PhotoSerializer,
    VideoSerializer,
    BookMarkSerializer,
)
from .utils import like_or_unlike
from core.permissions import IsMe


class KnowHowViewSet(ModelViewSet):
    queryset = KnowHowPost.objects.all()
    serializer_class = KnowHowPostSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsMe]
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)

    @action(detail=False, methods=["GET"])
    def knowhow_search(self, request):
        keyword = request.GET.get("keyword", None)
        # 제목 or 내용에 keyword가 포함된 object 필터링
        knowhow_list = KnowHowPost.objects.filter(
            Q(title__contains=keyword) | Q(content__contains=keyword)
        )

        # paginator
        paginator = self.paginator

        # 필터 되어 검색된 것이 있으면 return
        if len(knowhow_list):
            result = paginator.paginate_queryset(knowhow_list, request)
            serializer = KnowHowPostSerializer(result, many=True).data
            return paginator.get_paginated_response(serializer)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class PhotoViewSet(ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsMe]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)


class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsMe]
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)


class BookMarkViewSet(ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookMarkSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsMe]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)

    @action(methods=["GET"], detail=False)
    @permission_classes([IsMe])
    def mine(self, request):
        queryset = self.get_queryset().filter(user=self.request.user)
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST", "DELETE"])
def like_knowhow(request, pk):
    user = request.user
    response = like_or_unlike(KnowHowPost, user, pk)
    return response


@api_view(["POST", "DELETE"])
def like_photo(request, pk):
    user = request.user
    response = like_or_unlike(Photo, user, pk)
    return response


@api_view(["POST", "DELETE"])
def like_video(request, pk):
    user = request.user
    response = like_or_unlike(Video, user, pk)
    return response
