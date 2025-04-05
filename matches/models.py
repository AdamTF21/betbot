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
    start_time = models.DateTimeField(
        verbose_name='Начало тайма'
    )
    is_finished = models.BooleanField(
        default=False
    )
    result = models.CharField(
        max_length=20,
        choices=[('team1', 'Team 1'), ('team2', 'Team 2'), ('draw', 'Draw')],
        null=True,
        blank=True,
        verbose_name='Результат',

    )

    class Meta:
        verbose_name= 'Матч'
        verbose_name_plural= 'Матчи'
        ordering = ['-start_time']

    def str(self):
        return f"{self.team1} vs {self.team2} @ {self.start_time}"
