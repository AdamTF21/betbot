# betbot/urls.py
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from matches.views import MatchViewSet
from bets.views import BetViewSet
from users.views import RegisterTelegramUser

router = DefaultRouter()
router.register(r'matches', MatchViewSet, basename='match')
router.register(r'bets', BetViewSet, basename='bet')
router.register(r'users',RegisterTelegramUser, basename='user')
urlpatterns = [
    path('admin/', admin.site.urls),
    # API
    path('api/bets/', include('bets.urls')),
    path('api/users/', include('users.urls')),
    path('api/matches/', include('matches.urls')),


    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    # Docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(), name='swagger'),
]