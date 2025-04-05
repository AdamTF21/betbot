from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Bet


class BetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
        fields = 'all'

    def validate(self, data):
        user = self.context['request'].user
        profile = user.userprofile

        if profile.balance < data['amount']:
            raise serializers.ValidationError("Недостаточно средств!")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        amount = validated_data['amount']
        user_profile = user.userprofile
        user_profile.balance -= amount
        user_profile.save()
        return super().create(validated_data)