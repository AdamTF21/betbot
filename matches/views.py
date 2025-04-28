from django.db.models import Q

from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from .models import Match
from bets.models import Bet
from .serializers import MatchSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status




class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [AllowAny]

    def perform_update(self, serializer):
        old_instance = self.get_object()
        new_instance = serializer.save()

        if old_instance.winner != new_instance.winner and new_instance.winner:
            bets = Bet.objects.filter(match=new_instance)
            for bet in bets:
                if bet.chosen_winner == new_instance.winner:
                    profile = bet.user.profile
                    winnings = bet.amount * bet.odds
                    profile.balance += winnings
                    profile.save()


class MatchListAPIView(ListAPIView):
    queryset = Match.objects.filter(is_finished=False).order_by('start_time')
    serializer_class = MatchSerializer



class MatchSearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"detail": "Параметр запроса 'q' обязателен."}, status=status.HTTP_400_BAD_REQUEST)

        matches = Match.objects.filter(team1__icontains=query) | Match.objects.filter(team2__icontains=query)
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
