from rest_framework import serializers
from .models import CustomUser

from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "password"]

    def create(self, validated_data):
        user = CustomUser.objects.create(email=validated_data['email'], )
        user.set_password(validated_data['password'])
        user.save()
        return user
