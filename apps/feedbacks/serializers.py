from rest_framework.serializers import ModelSerializer

from feedbacks.models import FeedBack


class FeedBackSerializer(ModelSerializer):

    class Meta:
        model = FeedBack
        exclude = ("client", "master")
