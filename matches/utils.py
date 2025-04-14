from matches.models import Match
from bets.models import Bet


def calculate_bets(match: Match, winning_option_ids: list):
    bets = Bet.objects.filter(match=match)
    for bet in bets:
        if bet.option.id in winning_option_ids:
            bet.is_won = True
            bet.payout = bet.amount * bet.option.coefficient
            bet.user.balance += bet.payout
            bet.user.save()
        else:
            bet.is_won = False
        bet.save()
