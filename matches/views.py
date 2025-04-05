from django.shortcuts import render
from rest_framework import viewsets
from .models import Match
from .serializers import MatchSerializer
from rest_framework.permissions import AllowAny

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [AllowAny]


