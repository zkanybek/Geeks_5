from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import RegisterSerializer, ConfirmSerializer, LoginSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"message": "Код подтверждения отправлен", "code": user.confirmation_code},
            status=status.HTTP_201_CREATED
        )


class ConfirmView(generics.GenericAPIView):
    serializer_class = ConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        code = serializer.validated_data['code']
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

        if user.confirmation_code == code:
            user.is_active = True
            user.is_confirmed = True
            user.confirmation_code = None
            user.save()
            return Response({"message": "Подтверждено"})
        else:
            return Response({"error": "Неверный код"}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user and user.is_active and user.is_confirmed:
            return Response({"message": "Вы вошли в систему!"})
        return Response({"error": "Неверные данные или пользователь не подтвержден"}, status=status.HTTP_403_FORBIDDEN)