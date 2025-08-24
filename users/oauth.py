import os
import requests
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import GoogleLoginSerializer

User = get_user_model()


class GoogleLoginAPIView(CreateAPIView):
    serializer_class = GoogleLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']

        # Получаем access_token от Google
        token_response = requests.post(
            url="https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": os.environ.get('GOOGLE_CLIENT_ID'),
                "client_secret": os.environ.get('GOOGLE_CLIENT_SECRET'),
                "redirect_uri": os.environ.get('GOOGLE_REDIRECT_URI'),
                "grant_type": "authorization_code"
            }
        )

        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            return Response({"error": "Invalid access token!"}, status=400)

        # Получаем данные профиля
        user_info = requests.get(
            url="https://www.googleapis.com/oauth2/v3/userinfo",
            params={"alt": "json"},
            headers={"Authorization": f"Bearer {access_token}"}
        ).json()

        print(f"user_info {user_info}")

        email = user_info["email"]
        given_name = user_info.get("given_name", "")
        family_name = user_info.get("family_name", "")

        # Создаём или получаем пользователя
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": given_name,
                "last_name": family_name,
                "is_active": True  # активируем сразу, т.к. пришёл Google
            }
        )

        # Если юзер уже был, не перезаписываем имя/фамилию
        if not created:
            updated = False
            if not user.first_name and given_name:
                user.first_name = given_name
                updated = True
            if not user.last_name and family_name:
                user.last_name = family_name
                updated = True
            if not user.is_active:
                user.is_active = True
                updated = True
            if updated:
                user.save()

        # Генерируем JWT
        refresh = RefreshToken.for_user(user)
        refresh["email"] = user.email

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        })
