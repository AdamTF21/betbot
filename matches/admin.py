from django.contrib import admin
from .models import Match
from .utils import calculate_bets

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'team1', 'team2', 'winner')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.is_finished and obj.winner:
            winning_options = obj.bet_options.filter(option=obj.winner)
            winning_option_ids = list(winning_options.values_list('id', flat=True))
            calculate_bets(obj, winning_option_ids)


