from asgiref.sync import sync_to_async
from bets.models import Bet
from users.models import TelegramUser


@sync_to_async
def get_user_bet_history(telegram_id):
    try:
        user = TelegramUser.objects.get(telegram_id=telegram_id)
    except TelegramUser.DoesNotExist:
        return []

    bets = (
        Bet.objects
        .filter(user=user)
        .select_related("match", "option")
        .order_by("-id")
    )

    result = []
    for bet in bets:
        option_key = bet.option.option
        odds_field = f"{option_key}_odds"
        odds = getattr(bet.match, odds_field, 0)

        result.append({
            "id": bet.id,
            "amount": str(bet.amount),
            "match": {
                "team1": bet.match.team1,
                "team2": bet.match.team2,
            },
            "option": {
                "option": option_key,
                "odds": float(odds),
            },
        })

    return result
