from django.db import models

class Match(models.Model):
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    is_finished = models.BooleanField(default=False)
    result = models.CharField(
        max_length=20,
        choices=[('team1', 'Team 1'), ('team2', 'Team 2'), ('draw', 'Draw')],
        null=True,
        blank=True
    )

    def str(self):
        return f"{self.team1} vs {self.team2} @ {self.start_time}"
