from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal

from .models import Bet, Match, BetOption
from users.models import TelegramUser

from .serializers import BetSerializer, BetOptionSerializer


class BetHistoryView(APIView):
    def get(self, request, telegram_id):
        bets = Bet.objects.filter(user__telegram_id=telegram_id).order_by('-created_at')
        if not bets.exists():
            return Response({'detail': 'No bets found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BetSerializer(bets, many=True)
        return Response(serializer.data)


class BetCreateAPIView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        match_id = request.data.get("match_id")
        option_id = request.data.get("option_id")
        amount = request.data.get("amount")

        try:
            user = TelegramUser.objects.get(telegram_id=user_id)
            match = Match.objects.get(id=match_id)
            option = BetOption.objects.get(id=option_id)

            if user.balance < Decimal(amount):
                return Response({
                                    "detail": f"У вас недостаточно средств на балансе!\n Пажалуйста пополните свой баланс чтобы сделать ставку."},
                                status=400)

            user.balance -= Decimal(amount)
            user.save()

            bet = Bet.objects.create(
                user=user,
                match=match,
                option=option,
                amount=Decimal(amount),
            )

            return Response({"detail": "Ставка принята!"}, status=201)

        except TelegramUser.DoesNotExist:
            return Response({"detail": "Пользователь не найден"}, status=404)
        except Match.DoesNotExist:
            return Response({"detail": "Матч не найден"}, status=404)
        except BetOption.DoesNotExist:
            return Response({"detail": "Опция не найдена"}, status=404)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"detail": str(e)}, status=500)


class MatchOptionsAPIView(APIView):
    def get(self, request, match_id):
        try:
            match = Match.objects.get(id=match_id)
        except Match.DoesNotExist:
            return Response({"detail": "Матч не найден"}, status=status.HTTP_404_NOT_FOUND)

        options = BetOption.objects.filter(match=match)
        serializer = BetOptionSerializer(options, many=True)
        return Response(serializer.data)
