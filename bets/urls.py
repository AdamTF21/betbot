from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BetHistoryView, BetCreateAPIView, MatchOptionsAPIView

router = DefaultRouter()

urlpatterns = [

    path('matches/<int:match_id>/options/', MatchOptionsAPIView.as_view(), name='match-options'),
    path('history/<int:telegram_id>/', BetHistoryView.as_view(), name='history'),
    path('create/', BetCreateAPIView.as_view(), name='create-bet'),
    path('', include(router.urls)),
]
