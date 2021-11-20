from rest_framework import serializers
from .models import KnowHowPost, KnowHowPostImage, Photo, Video, Bookmark

# TODO: UserSerializer 추가해서 user의 이메일 정보 볼 수 있도록 변경
# image추가 만들기


class KnowHowImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = KnowHowPostImage
        fields = ("image",)


class KnowHowPostSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField("is_like_field")

    class Meta:
        model = KnowHowPost
        fields = ("id", "user", "title", "content", "is_like", "images")

    def is_like_field(self, post):
        if "request" in self.context:
            user = self.context["request"].user
            return post.like.filter(id=user.pk).exists()
        else:
            return False

    def create(self, validated_data):
        instance = KnowHowPost.objects.create(**validated_data)
        image_set = self.context["request"].FILES
        for image_data in image_set.getlist("image"):
            KnowHowPostImage.objects.create(post=instance, image=image_data)
        return instance

    def get_images(self, obj):
        image = obj.knowhow_image.all()
        return KnowHowImageSerializer(
            instance=image, many=True, context=self.context
        ).data


# TODO: 사진과 동영상은 각각 크기는 어느 정도로?
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("id", "user", "photo", "description")
        read_only_fields = ("id", "user")


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ("id", "user", "video", "description")
        read_only_fields = ("id", "user")


class BookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ("id", "user", "name", "urls")
        read_only_fields = ("id", "user")
