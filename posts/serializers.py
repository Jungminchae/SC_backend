from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField
from users.serializers import UserSerializer
from .models import KnowHowPost, KnowHowPostImage, Photo, PhotoImage, Video, Bookmark
from .utils import tag_save



class KnowhowImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = KnowHowPostImage
        fields = ("image",)

# TODO: UserSerializer 추가해서 user의 이메일 정보 볼 수 있도록 변경
class KnowHowPostSerializer(TaggitSerializer, serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_like = serializers.SerializerMethodField("is_like_field")
    images = serializers.SerializerMethodField()
    tags = TagListSerializerField()  # ["이렇게","저렇게"] 보내야함

    class Meta:
        model = KnowHowPost
        fields = (
            "id",
            "user",
            "title",
            "content",
            "is_like",
            "cover",
            "tags",
            "only_me",
            "images"
        )

    def get_images(self, obj):
        image = obj.knowhow_image.all()
        return KnowhowImageSerializer(
            instance=image, many=True, context=self.context
        ).data

    def is_like_field(self, post):
        if "request" in self.context:
            user = self.context["request"].user
            return post.like.filter(id=user.pk).exists()
        else:
            return False

    def create(self, validated_data):
        obj = tag_save(self, validated_data)
        return obj


class PhotoImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = PhotoImage
        fields = ("image",)


# TODO: 사진과 동영상은 각각 크기는 어느 정도로?
class PhotoSerializer(TaggitSerializer, serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    images = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField("is_like_field")
    tags = TagListSerializerField()  # ["이렇게","저렇게"] 보내야함

    class Meta:
        model = Photo
        fields = ("id", "user", "images", "is_like", "description", "tags", "only_me")
        read_only_fields = ("id", "user")

    def is_like_field(self, post):
        if "request" in self.context:
            user = self.context["request"].user
            return post.like.filter(id=user.pk).exists()
        else:
            return False

    def get_images(self, obj):
        image = obj.photo_image.all()
        return PhotoImageSerializer(
            instance=image, many=True, context=self.context
        ).data

    def create(self, validated_data):
        obj = tag_save(self, validated_data)
        image_set = self.context["request"].FILES
        for image_data in image_set.getlist("image"):
            PhotoImage.objects.create(post=obj, image=image_data)
        return obj


class VideoSerializer(TaggitSerializer, serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_like = serializers.SerializerMethodField("is_like_field")
    tags = TagListSerializerField()

    class Meta:
        model = Video
        fields = ("id", "user", "video", "is_like", "description", "tags", "only_me")
        read_only_fields = ("id", "user")

    def is_like_field(self, post):
        if "request" in self.context:
            user = self.context["request"].user
            return post.like.filter(id=user.pk).exists()
        else:
            return False

    def create(self, validated_data):
        obj = tag_save(self, validated_data)
        return obj


class BookMarkSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = ("id", "user", "name", "urls")
        read_only_fields = ("id", "user")
