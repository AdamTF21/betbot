from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MatchViewSet, MatchListAPIView, BetOptionViewSet

router = DefaultRouter()
router.register(r'', MatchViewSet, basename='match')
router.register(r'', BetOptionViewSet, basename='bets')

urlpatterns = [
    path('', include(router.urls)),
    path('', MatchListAPIView.as_view(), name='match-list'),
]