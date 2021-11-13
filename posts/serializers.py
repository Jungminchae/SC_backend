from rest_framework import serializers
from .models import KnowHowPost, KnowHowPostImage


class KnowHowImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = KnowHowPostImage
        fields = ("image",)


class KnowHowPostSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = KnowHowPost
        fields = ("id", "user", "title", "content", "like", "images")

    def create(self, validated_data):
        instance = KnowHowPost.objects.create(**validated_data)
        image_set = self.context["request"].FILES
        for image_data in image_set.getlist("image"):
            KnowHowPostImage.objects.create(post=instance, image=image_data)
        return instance

    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        image = obj.images.all()
        return KnowHowImageSerializer(instance=image, many=True).data
