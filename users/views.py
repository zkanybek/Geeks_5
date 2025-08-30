from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from users.models import CustomUser

from .serializers import (
    RegisterValidateSerializer,
    AuthValidateSerializer,
    ConfirmationSerializer
)
from .models import ConfirmationCode
import random
import string
from users.serializers import CustomTokenOptainSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.core.cache import cache



class AuthorizationAPIView(CreateAPIView):
    serializer_class = AuthValidateSerializer
    def post(self, request):
        serializer = AuthValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user:
            if not user.is_active:
                return Response(
                    status=status.HTTP_401_UNAUTHORIZED,
                    data={'error': 'User account is not activated yet!'}
                )

            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})

        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
            data={'error': 'User credentials are wrong!'}
        )

class RegistrationAPIView(CreateAPIView):
    serializer_class = RegisterValidateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        with transaction.atomic():
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                is_active=False
            )

            # Генерация 6-значного кода
            code = ''.join(random.choices(string.digits, k=6))

            # Сохраняем код в Redis с TTL = 300 секунд (5 минут)
            cache.set(f"confirm_code:{user.id}", code, timeout=300)

        return Response(
            status=status.HTTP_201_CREATED,
            data={
                'user_id': user.id,
                'confirmation_code': code  
            }
        )


class ConfirmUserAPIView(CreateAPIView):
    serializer_class = ConfirmationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        code = serializer.validated_data['code']

        stored_code = cache.get(f"confirm_code:{user_id}")
        if not stored_code:
            return Response({"error": "Код просрочен или не существует!"}, status=400)

        if stored_code != code:
            return Response({"error": "Неверный код!"}, status=400)

        with transaction.atomic():
            user = CustomUser.objects.get(id=user_id)
            user.is_active = True
            user.save()

            token, _ = Token.objects.get_or_create(user=user)

            cache.delete(f"confirm_code:{user_id}")

        return Response(
            status=status.HTTP_200_OK,
            data={
                'message': 'User аккаунт успешно активирован',
                'key': token.key
            }
        )

class CustomTokenOptainPairView(TokenObtainPairView):
    serializer_class = CustomTokenOptainSerializer