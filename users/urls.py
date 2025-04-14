from django.urls import path
from .views import RegisterTelegramUser, BalanceView, DepositView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', RegisterTelegramUser, basename='user')

urlpatterns = [
    path('register/', RegisterTelegramUser.as_view(), name='register'),
    path('balance/', BalanceView.as_view(), name='balance'),
    path('deposit/', DepositView.as_view(), name='deposit'),
]