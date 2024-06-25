from PIL import Image
from django.http.response import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from grapes_backend_app.models import SenseQueryModel, ResultModel
from grapes_backend_app.serializer import SenseQuerySerializer, ResultModelSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

import cv2
import grapes_backend_app.inference as inference

@api_view(['POST'])
@permission_classes([AllowAny])
def manage_sensors_query(request):
  
  received_data_serializer = SenseQuerySerializer(request.POST, request.FILES)

  if not (received_data_serializer.is_valid()):
    return JsonResponse(received_data_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
  
  result = inference.predict(request.FILES["image"])
  img_str = cv2.imencode('.jpg', result)[1].tostring()
  return HttpResponse(
    img_str,
    status = status.HTTP_200_OK
  )


def save_image(name: str, file: any) -> None:
  with open(name, 'wb+') as destino:
    for chunk in file.chunks():
      destino.write(chunk)