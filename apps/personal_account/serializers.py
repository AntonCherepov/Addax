from rest_framework import serializers

from personal_account.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("type_code", "status_code")
