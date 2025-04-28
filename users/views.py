
from django.http import Http404
import logging
from .serializers import TelegramUserSerializer, BalanceSerializer
from decimal import Decimal

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import TelegramUser
from users.serializers import TelegramUserSerializer



class RegisterUserView(APIView):
    def post(self, request):
        serializer = TelegramUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetUserView(APIView):
    def get(self, request, telegram_id):
        try:
            user = TelegramUser.objects.get(telegram_id=telegram_id)
            serializer = TelegramUserSerializer(user)
            return Response(serializer.data)
        except TelegramUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)





logger = logging.getLogger(__name__)

class BalanceView(APIView):
    def get_permissions(self):
        if self.kwargs.get('telegram_id'):
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, telegram_id=None):
        logger.info(f"Request for telegram_id: {telegram_id}, user: {request.user}")
        if telegram_id:
            try:
                user = TelegramUser.objects.get(telegram_id=telegram_id)
            except TelegramUser.DoesNotExist:
                logger.error(f"No user found for telegram_id: {telegram_id}")
                raise Http404("Пользователь с таким Telegram ID не найден")
        else:
            if not request.user.is_authenticated:
                return Response({'error': 'Пользователь не аутентифицирован'}, status=401)
            user = request.user

        serializer = BalanceSerializer(user)
        return Response(serializer.data)

    def post(self, request, telegram_id=None):
        if telegram_id:
            try:
                user = TelegramUser.objects.get(telegram_id=telegram_id)
            except TelegramUser.DoesNotExist:
                logger.error(f"No user found for telegram_id: {telegram_id}")
                raise Http404("Пользователь с таким Telegram ID не найден")
        else:
            if not request.user.is_authenticated:
                return Response({'error': 'Пользователь не аутентифицирован'}, status=401)
            user = request.user

        amount = request.data.get('amount')

        try:
            amount = float(amount)
        except (ValueError, TypeError):
            return Response({'error': 'Неверная сумма'}, status=400)

        if amount <= 0:
            return Response({'error': 'Сумма должна быть положительной'}, status=400)

        user.balance += amount
        user.save()
        return Response({'balance': user.balance})


class DepositView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        amount = request.data.get("amount")

        if not user_id or not amount:
            return Response({"detail": "Нужны user_id и amount"}, status=400)

        try:
            user = TelegramUser.objects.get(telegram_id=user_id)
            user.balance += Decimal(amount)
            user.save()

            return Response({"detail": "Баланс успешно пополнен!", "balance": str(user.balance)}, status=200)

        except TelegramUser.DoesNotExist:
            return Response({"detail": "Пользователь не найден"}, status=404)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"detail": str(e)}, status=500)
