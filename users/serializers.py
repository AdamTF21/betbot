
from .models import TelegramUser
from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ('id', 'first_name', 'last_name', 'telegram_id', 'balance')



class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['telegram_id', 'first_name', 'last_name', 'balance']





class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['balance']