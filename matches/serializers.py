from rest_framework import serializers
from .models import Match


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'team1', 'team2', 'start_time', 'chance_team1', 'chance_team2', 'chance_draw', 'odds_team1',
                  'odds_team2', 'odds_draw']





