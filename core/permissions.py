from rest_framework.permissions import BasePermission


# 오직 나만 수정 가능
class IsMe(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOnlyMyPost(BasePermission):
    def has_object_permission(self, request, view, obj):
        # 나만보기 일 때, 내가 아니면 False
        if obj.only_me is True and request.user == obj.user:
            return True
        # 전체공개 일 때, True
        elif obj.only_me is False:
            return True
        else:
            return False
