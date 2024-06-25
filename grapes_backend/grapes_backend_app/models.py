from django.utils import timezone
from django.db import models

class SenseQueryModel(models.Model):
  date_time = models.DateTimeField(default = timezone.now)
  ph = models.FloatField()
  image = models.FileField(upload_to='images/')

class ResultModel(models.Model):
  annotated_image = models.FileField()
  brix_estimation = models.FloatField()
  maturity = models.CharField(max_length = 12)