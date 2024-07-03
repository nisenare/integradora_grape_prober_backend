from PIL import Image
from django.http.response import JsonResponse, HttpResponse
from django.core import serializers
from rest_framework.parsers import JSONParser
from rest_framework import status
from grapes_backend_app.models import PredictionModel, SenseQueryModel
from grapes_backend_app.serializer import SenseQuerySerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

import grapes_backend_app.inference as inference

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
  result_model.save()
  return JsonResponse(
    result,
    status = status.HTTP_200_OK,
  )