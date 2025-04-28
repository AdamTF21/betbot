from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Match
from bets.models import BetOption


@receiver(post_save, sender=Match)
def create_bet_options(sender, instance, created, **kwargs):
    if created:
        BetOption.objects.bulk_create([
            BetOption(match=instance, option='team1'),
            BetOption(match=instance, option='draw'),
            BetOption(match=instance, option='team2'),
        ])
