from django.db import models


class Match(models.Model):
    team1 = models.CharField(
        max_length=100,
        verbose_name='Kоманда:1'
    )
    team2 = models.CharField(
        max_length=100,
        verbose_name='Kоманда:2'
    )
    chance_team1 = models.CharField(
        max_length=5,
        verbose_name='Шансы команды_1'
    )
    chance_team2 = models.CharField(
        max_length=5,
        verbose_name='Шансы команды_2'
    )
    chance_draw = models.CharField(
        max_length=5,
        verbose_name='Шансы ничьи'
    )
    odds_team1 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Коэффициенты команды_1'
    )
    odds_team2 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Коэффициенты команды_2'
    )
    odds_draw = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Коэффициенты ничьи'
    )
    start_time = models.DateTimeField(
        max_length=20,
        verbose_name='Начало тайма'
    )
    is_finished = models.BooleanField(
        default=False,
    )
    WINNER_CHOICES = (
        ('team1', 'Team 1'),
        ('team2', 'Team 2'),
        ('draw', 'Draw'),
    )
    winner = models.CharField(
        max_length=10,
        choices=WINNER_CHOICES,
        null=True, blank=True
    )
    notified = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчи'
        ordering = ['-start_time']

    def __str__(self):
        return f"{self.team1} vs {self.team2} @ {self.start_time}"
