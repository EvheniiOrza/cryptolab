from django.db import models
from django.contrib.auth.models import User

class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_number = models.IntegerField()
    attempts_left = models.IntegerField()
    is_active = models.BooleanField(default=True)
    result = models.CharField(max_length=10, choices=[('Win', 'Win'), ('Lose', 'Lose')], null=True)
    created_at = models.DateTimeField(auto_now_add=True)
