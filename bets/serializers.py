from rest_framework import serializers
from .models import Bet, BetOption


class BetSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    match_id = serializers.IntegerField(write_only=True)
    option_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Bet
        fields = ['id', 'amount', 'user_id', 'match_id', 'option_id']
        read_only_fields = ['id', 'user', 'match', 'option']


class BetOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BetOption
        fields = ['id', 'name', 'coefficient']
