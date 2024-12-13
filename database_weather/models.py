# weather/models.py
from django.db import models

class WeatherQuery(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
