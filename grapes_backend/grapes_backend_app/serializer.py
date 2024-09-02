from django import forms
from rest_framework import serializers
from grapes_backend_app.models import SenseQueryModel, PredictionModel
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('id', 'username','email', 'password')


class SenseQuerySerializer(forms.ModelForm):
  class Meta:
    model = SenseQueryModel
    fields = ("id", "date_time", "ph", "image")


class PredictionModelSerializer(forms.ModelForm):
  class Meta:
    model = PredictionModel
    fields = ("id", "date_time", "ph", "overall_maturity", "annotated_image")

