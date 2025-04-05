from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from users.models import UserProfile
from .models import Bet
from .serializers import BetSerializer

class BetViewSet(viewsets.ModelViewSet):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        profile = UserProfile.objects.get(user=user)

        bet_amount = serializer.validated_data['amount']

        if profile.balance < bet_amount:
            raise serializers.ValidationError("Недостаточно средств!")

        profile.balance -= bet_amount
        profile.save()
        serializer.save(user=user)
