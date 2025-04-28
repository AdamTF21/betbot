from django.contrib import admin
from .models import Bet


@admin.register(Bet)
class BetsAdmin(admin.ModelAdmin):
    list_display = ['id', 'match', 'user__first_name', 'user__last_name', 'option', 'amount']
