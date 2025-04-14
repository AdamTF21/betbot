from django.db import models
from django.conf import settings
from matches.models import Match, BetOption


class Bet(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        verbose_name='Матч'
    )
    option = models.ForeignKey(BetOption, on_delete=models.CASCADE)
    chosen_winner = models.CharField(
        max_length=20,
        choices=[('team1', 'Team 1'), ('team2', 'Team 2'), ('draw', 'Draw')],
        verbose_name='Выбранный победитель'
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
    payout = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )


    class Meta:
        verbose_name= 'Ставка'
        verbose_name_plural= 'Ставки'
        ordering = ['-amount']


    def __str__(self):
        return f"{self.user.username} поставил на {self.chosen_winner} — {self.amount} руб."