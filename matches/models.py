from django.core.validators import MinValueValidator
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
    odds_team1 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    odds_draw = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    odds_team2 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    start_time = models.DateTimeField(
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


    class Meta:
        verbose_name= 'Матч'
        verbose_name_plural= 'Матчи'
        ordering = ['-start_time']

    def __str__(self):
        return f"{self.team1} vs {self.team2} @ {self.start_time}"



class BetOption(models.Model):
    match = models.ForeignKey(
        Match,
        related_name='bet_options',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=255
    )
    coefficient = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.name} ({self.coefficient})"
