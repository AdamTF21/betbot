from django.contrib import admin
from .models import TelegramUser

@admin.register(TelegramUser)
class User(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'telegram_id', 'balance' )








