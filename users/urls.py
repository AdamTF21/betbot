from django.urls import path
from .views import RegisterAPIView, BalanceView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('balance/', BalanceView.as_view(), name='balance'),
]