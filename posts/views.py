from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .models import KnowHowPost
from .serializers import KnowHowPostSerializer
from .permissions import IsMe


# TODO
# User 모델이랑 Profile모델이랑 헷갈림 수정 필요
class KnowHowViewSet(ModelViewSet):

    queryset = KnowHowPost.objects.all()
    serializer_class = KnowHowPostSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]
        elif self.action == "create":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsMe]
        return [permission() for permission in permission_classes]

    # Knowhow 쓰기
    def create(self, request):
        # 로그인 상태의 유저만 질문하기 가능 - 기본 permission IsAuthenticated
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = KnowHowPostSerializer(data=request.data)
        # 유효성검사
        if serializer.is_valid():
            knowhow = serializer.save(user=request.user)
            knowhow_serializer = KnowHowPostSerializer(knowhow).data
            return Response(data=knowhow_serializer, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
