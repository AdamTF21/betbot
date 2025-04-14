from rest_framework import viewsets, serializers
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from users.models import TelegramUser
from .models import Bet
from .serializers import BetSerializer

class BetViewSet(viewsets.ModelViewSet):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='my')
    def my_bets(self, request):
        user = request.user
        bets = Bet.objects.filter(user=user)
        serializer = self.get_serializer(bets, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        profile = TelegramUser.objects.get(user=user)

        bet_amount = serializer.validated_data['amount']

        if profile.balance < bet_amount:
            raise serializers.ValidationError("Недостаточно средств!")

        profile.balance -= bet_amount
        profile.save()
        serializer.save(user=user)


class BetCreateAPIView(CreateAPIView):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)