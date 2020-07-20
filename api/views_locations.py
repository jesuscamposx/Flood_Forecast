from api.models import Calle, Alcaldia, Colonia
from api.serializers import CalleSerializer, AlcaldiaSerializer, ColoniaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework import status
import logging

class CalleView(APIView):
    def get(self, request, format=None):
        id_colonia = self.request.query_params.get('colonia', None)
        if id_colonia is None:
            return Response({"id": 40001, "text": "Colonia es necesario."},
                            status=status.HTTP_400_BAD_REQUEST)
        calles = Calle.objects.all().filter(colonia=id_colonia)
        serializer = CalleSerializer(calles, many=True)
        return Response(serializer.data)

class AlcaldiaView(APIView):
    def get(self, request, format=None):
        alcaldias = Alcaldia.objects.all()
        serializer = AlcaldiaSerializer(alcaldias, many=True)
        return Response(serializer.data)

class ColoniaView(APIView):
    def get(self, request, format=None):
        colonias = Colonia.objects.all()
        serializer = ColoniaSerializer(colonias, many=True)
        return Response(serializer.data)
