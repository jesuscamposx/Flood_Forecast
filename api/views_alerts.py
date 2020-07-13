from api.models import Destinatario
from api.serializers import DestinatarioSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework import status
import logging


class DestinatarioView(APIView):
    def post(self, request, format=None):
        serializer = DestinatarioSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
