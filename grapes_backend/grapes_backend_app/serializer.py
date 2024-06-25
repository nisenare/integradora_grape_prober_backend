from django import forms
from rest_framework import serializers
from grapes_backend_app.models import SenseQueryModel, ResultModel

class SenseQuerySerializer(forms.ModelForm):
  class Meta:
    model = SenseQueryModel
    fields = ("id", "date_time", "ph", "image")

class ResultModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = ResultModel
    fields = ("id", "annotated_image", "brix_estimation", "maturity")

