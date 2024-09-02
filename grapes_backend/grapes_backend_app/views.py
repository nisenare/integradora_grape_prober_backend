from PIL import Image
from django.http.response import JsonResponse, HttpResponse
from django.core import serializers
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.parsers import JSONParser
from rest_framework import status
from grapes_backend_app.models import PredictionModel, SenseQueryModel
from grapes_backend_app.serializer import SenseQuerySerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
import grapes_backend_app.inference as inference
import cv2
import numpy as np
import base64

@api_view(['POST'])
@permission_classes([AllowAny])
def manage_sensors_query(request):
  received_data_serializer = SenseQuerySerializer(request.POST, request.FILES)

  if not (received_data_serializer.is_valid()):
    return JsonResponse(received_data_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
  
  result = inference.predict(request.FILES["image"], request.POST["ph"])
  result_model = PredictionModel(
    date_time = result["date_time"],
    annotated_image = result["annotated_image"],
    overall_maturity = result["overall_maturity"],
    ph = result["ph"]
  )
  save_prediction(result_model)
    
  return JsonResponse(
    result,
    status = status.HTTP_200_OK,
  )


def save_prediction(result_model):
  if not (result_model.overall_maturity == "None"):
    image_data = base64.b64decode(result_model.annotated_image)
    np_array = np.frombuffer(image_data, np.uint8)
    im = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    result_model.annotated_image = base64.b64encode(
      cv2.imencode('.jpg', im)[1]
    ).decode('utf-8')
    result_model.save()

# Vistas HTTP
def home(request):
  return redirect("login_form")


def login(request):
  return render(request, "grapes_backend_app/login_form.html", {})


@login_required
def base_header(request):
  return render(request, "grapes_backend_app/base_header.html", {})


@login_required
def dashboard(request, page_num):
  predictions = PredictionModel.objects.all().order_by("-date_time")
  paginator = Paginator(predictions, per_page = 10)
  page = paginator.get_page(page_num)
  context = {
    "predictions": page,
    "page": {
      "page_range": paginator.get_elided_page_range(
        on_ends = 1,
        on_each_side = 2,
        number = 1,
      ),
      "prev_page": (page.number - 1) if page.has_previous() else page.number,
      "next_page": (page.number + 1) if page.has_next() else page.number,
      "current": page.number,
      "has_next": page.has_next(),
      "has_previous": page.has_previous()
    },
  }
  
  return render(request, "grapes_backend_app/dashboard.html", context)