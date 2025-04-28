from django.contrib import admin
from .models import Match
from bets.models import BetOption
from .utils import calculate_bets


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'team1', 'team2', 'winner')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.is_finished and obj.winner:
            try:
                winning_option = obj.bet_options.get(option=obj.winner)
                calculate_bets(obj, winning_option.id)
            except BetOption.DoesNotExist:
                pass



