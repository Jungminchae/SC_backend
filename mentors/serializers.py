from rest_framework.serializers import ModelSerializer
from mentors.models import Mentor


class MentorSerializer(ModelSerializer):
    class Meta:
        model = Mentor
