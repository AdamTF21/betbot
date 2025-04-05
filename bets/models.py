from django.db import models
from django.conf import settings
from matches.models import Match

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
    odds = models.FloatField()
    is_won = models.BooleanField(null=True, blank=True)

    class Meta:
        verbose_name= 'Ставка'
        verbose_name_plural= 'Ставки'
        ordering = ['-amount']


    def str(self):
        return f"{self.user.username} поставил на {self.chosen_winner} — {self.amount} руб."