from rest_framework import serializers
from .models import Match, BetOption


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'team1', 'team2', 'start_time', 'odds_team1', 'odds_draw',  'odds_team2']

class BetOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BetOption
        fields = "__all__"