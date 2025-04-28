from attr.filters import include
from django.urls import path
from .views import RegisterUserView, GetUserView, BalanceView, DepositView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', RegisterUserView, basename='user')

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('register/<int:telegram_id>/',GetUserView.as_view() , name='get-user'),
    path('balance/<int:telegram_id>/', BalanceView.as_view(), name='balance_by_telegram_id'),
    path('deposit/', DepositView.as_view(), name='deposit'),

]