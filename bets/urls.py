from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BetViewSet, BetCreateAPIView

router = DefaultRouter()
router.register(r'user-bets', BetViewSet, basename='user-bets')

urlpatterns = [
    path('', include(router.urls)),
    path('create/', BetCreateAPIView.as_view(), name='create-bet'),
]