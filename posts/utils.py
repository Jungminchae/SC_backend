from rest_framework.response import Response
from rest_framework import status
from taggit.serializers import TaggitSerializer


def tag_save(self, validated_data):
    tag_validated_data = validated_data.copy()
    to_be_tagged, tag_validated_data = self._pop_tags(tag_validated_data)
    tag_object = super(TaggitSerializer, self).create(tag_validated_data)
    obj = self._save_tags(tag_object, to_be_tagged)
    return obj


def like_or_unlike(model, user, pk):
    instance = model.objects.get(id=pk)
    if user in instance.like.all():
        instance.like.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        instance.like.add(user)
        return Response(status=status.HTTP_201_CREATED)
