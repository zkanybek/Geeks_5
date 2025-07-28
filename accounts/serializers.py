# accounts/serializers.py
from rest_framework import serializers
from .models import CustomUser
import random


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            is_active=False,
            is_confirmed=False,
            confirmation_code=str(random.randint(100000, 999999))
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
