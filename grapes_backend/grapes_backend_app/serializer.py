from django import forms
from rest_framework import serializers
from grapes_backend_app.models import SenseQueryModel, PredictionModel

class SenseQuerySerializer(forms.ModelForm):
  class Meta:
    model = SenseQueryModel
    fields = ("id", "date_time", "ph", "image")


class PredictionModelSerializer(forms.ModelForm):
  class Meta:
    model = PredictionModel
    fields = ("id", "date_time", "ph", "overall_maturity", "annotated_image")

