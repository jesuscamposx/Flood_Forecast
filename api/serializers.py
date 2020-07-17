from rest_framework import serializers
from api.models import Alcaldia, Colonia, Calle, Condicion
from api.models import Sensor, Medicion, Destinatario


class AlcaldiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alcaldia
        fields = ['id_alcaldia', 'nombre', 'latitud', 'longitud',]


class ColoniaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colonia
        fields = ['id_colonia', 'nombre', 'codigo_postal', 'latitud',
                  'longitud', 'id_alcaldia']


class CalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calle
        fields = ['id_calle', 'nombre', 'latitud', 'longitud', 'id_colonia']


class CondicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condicion
        fields = ['fecha', 'id_alcaldia', 'precipitacion', 'temp_min',
                  'temp_max', 'inundacion', 'creado', 'actualizado']


class SensorSerializer(serializers.ModelSerializer):
    calle = CalleSerializer(read_only=True)
    class Meta:
        model = Sensor
        fields = ['id_sensor', 'activado', 'latitud', 'longitud', 'calle']


class MedicionSerializer(serializers.ModelSerializer):
    sensor = SensorSerializer(read_only=True)
    class Meta:
        model = Medicion
        fields = ['id_medicion', 'creado', 'nivel_agua', 'sensor']


class DestinatarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destinatario
        fields = ['email', 'creado', 'nombre', 'apellido']
