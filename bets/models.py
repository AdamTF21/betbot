from django.db import models
from django.conf import settings
from matches.models import Match
from django.utils import timezone


class BetOption(models.Model):
    OPTION_CHOICES = (
        ('team1', 'Team 1'),
        ('team2', 'Team 2'),
        ('draw', 'Draw'),
    )

    match = models.ForeignKey(
        Match,
        related_name='bet_options',
        on_delete=models.CASCADE
    )
    option = models.CharField(
        max_length=10,
        choices=OPTION_CHOICES,

    )

    def get_coefficient(self):
        if self.option == 'team1':
            return self.match.odds_team1
        elif self.option == 'team2':
            return self.match.odds_team2
        elif self.option == 'draw':
            return self.match.odds_draw
        return None

    def __str__(self):
        return f"{self.option} ({self.get_coefficient()})"


class Bet(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        verbose_name='Матч',
        related_name='bets'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма'

    )
    is_won = models.BooleanField(
        null=True,
        blank=True
    )
    option = models.ForeignKey(
        BetOption,
        on_delete=models.CASCADE,

    )
    payout = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    created_at = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        verbose_name = 'Ставка'
        verbose_name_plural = 'Ставки'
        ordering = ['-amount']

    def __str__(self):
        return f"{self.user} поставил на {self.option} — {self.amount}c."
