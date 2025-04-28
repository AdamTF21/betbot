from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MatchViewSet, MatchListAPIView, MatchSearchAPIView

router = DefaultRouter()
router.register(r'', MatchViewSet, basename='match')

urlpatterns = [
    path('list/', MatchListAPIView.as_view(), name='match-list'),
    path('search/', MatchSearchAPIView.as_view(), name='match-search'),
    path('', include(router.urls)),
]
