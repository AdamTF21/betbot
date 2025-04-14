from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import TelegramUser
from .serializers import TelegramUserSerializer, BalanceSerializer


class RegisterTelegramUser(APIView):
    def post(self, request):
        telegram_id = request.data.get("telegram_id")
        username = request.data.get("username")

        user, created = TelegramUser.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={"username": username}
        )
        serializer = TelegramUserSerializer(user)
        return Response(serializer.data)


class BalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.userprofile
        serializer = BalanceSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        profile = request.user.userprofile
        amount = request.data.get('amount')

        try:
            amount = float(amount)
        except (ValueError, TypeError):
            return Response({'error': 'Неверная сумма'}, status=400)

        if amount <= 0:
            return Response({'error': 'Сумма должна быть положительной'}, status=400)

        profile.balance += amount
        profile.save()
        return Response({'balance': profile.balance})


class DepositView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        profile = request.user.profile
        profile.balance += int(amount)
        profile.save()
        return Response({'balance': profile.balance})