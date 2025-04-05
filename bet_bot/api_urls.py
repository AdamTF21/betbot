
from rest_framework.routers import DefaultRouter
from django.urls import include, path
from matches.views import MatchViewSet
from bets.views import BetViewSet


router = DefaultRouter()
router.register(r'matches', MatchViewSet, basename='match')
router.register(r'bets', BetViewSet, basename='bet')

urlpatterns = [
    path('', include(router.urls)),
    path('users/', include('users.urls')),
]
