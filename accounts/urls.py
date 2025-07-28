from django.urls import path
from .views import RegisterView, ConfirmView, LoginView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm/', ConfirmView.as_view(), name='confirm'),
    path('login/', LoginView.as_view(), name='login'),
]
