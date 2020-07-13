from rest_framework import serializers
from api.models import Alcaldia, Colonia, Calle, Condicion
from api.models import Sensor, Medicion, Destinatario


class AlcaldiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alcaldia
        fields = ['id_alcaldia', 'nombre', 'altitud', 'latitud']


class ColoniaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colonia
        fields = ['id_colonia', 'nombre', 'codigo_postal', 'altitud',
                  'latitud', 'id_alcaldia']


class CalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calle
        fields = ['id_calle', 'nombre', 'altitud', 'latitud', 'id_colonia']


class CondicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condicion
        fields = ['fecha', 'id_alcaldia', 'precipitacion', 'temp_min',
                  'temp_max', 'inundacion', 'creado', 'actualizado']


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id_sensor', 'activado', 'altitud', 'latitud', 'id_calle']


class MedicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicion
        fields = ['id_medicion', 'creado', 'nivel_agua', 'id_sensor']


class DestinatarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destinatario
        fields = ['email', 'creado', 'nombre', 'apellido']
