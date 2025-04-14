
from .models import TelegramUser
from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ('id', 'username', 'telegram_id', 'balance')



class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['telegram_id', 'username', 'balance']





class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['username']