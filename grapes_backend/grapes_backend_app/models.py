from django.utils import timezone
from django.db import models

class SenseQueryModel(models.Model):
  date_time = models.DateTimeField(default = timezone.now)
  ph = models.FloatField()
  image = models.FileField(upload_to='images/')


class PredictionModel(models.Model):
  date_time = models.DateTimeField(default = timezone.now)
  annotated_image = models.TextField()
  overall_maturity = models.CharField(max_length = 11)
  ph = models.FloatField()
