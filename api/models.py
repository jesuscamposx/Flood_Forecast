from django.db import models


class Alcaldia(models.Model):
    id_alcaldia = models.AutoField(db_column='idAlcaldia', primary_key=True)
    nombre = models.CharField(max_length=45)
    altitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # noqa
    latitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # noqa

    class Meta:
        managed = False
        db_table = 'alcaldia'


class Colonia(models.Model):
    id_colonia = models.AutoField(db_column='idColonia', primary_key=True)
    nombre = models.CharField(max_length=45)
    codigo_postal = models.CharField(db_column='codigoPostal', max_length=45, blank=True, null=True)  # noqa
    altitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # noqa
    latitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # noqa
    id_alcaldia = models.ForeignKey(Alcaldia, models.CASCADE, db_column='idAlcaldia')  # noqa

    class Meta:
        managed = False
        db_table = 'colonia'


class Calle(models.Model):
    id_calle = models.AutoField(db_column='idCalle', primary_key=True)
    nombre = models.CharField(max_length=45)
    altitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # noqa
    latitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # noqa
    id_colonia = models.ForeignKey('Colonia', models.CASCADE, db_column='idColonia')  # noqa

    class Meta:
        managed = False
        db_table = 'calle'


class Condicion(models.Model):
    fecha = models.DateField(primary_key=True)
    id_alcaldia = models.ForeignKey(Alcaldia, models.DO_NOTHING, db_column='idAlcaldia')  # noqa
    precipitacion = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # noqa
    temp_min = models.DecimalField(db_column='tempMin', max_digits=5, decimal_places=2, blank=True, null=True)  # noqa
    temp_max = models.DecimalField(db_column='tempMax', max_digits=5, decimal_places=2, blank=True, null=True)  # noqa
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'condicion'
        unique_together = (('fecha', 'idalcaldia'),)


class Inundacion(models.Model):
    id_inundacion = models.AutoField(db_column='idInundacion', primary_key=True)  # noqa
    fecha = models.ForeignKey(Condicion, models.DO_NOTHING, db_column='fecha')
    id_alcaldia = models.ForeignKey(Condicion, models.DO_NOTHING, db_column='idAlcaldia')  # noqa
    indicador = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inundacion'


class Sensor(models.Model):
    id_sensor = models.AutoField(db_column='idSensor', primary_key=True)
    activado = models.IntegerField(default=True)
    altitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # noqa
    latitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # noqa
    id_calle = models.ForeignKey(Calle, models.DO_NOTHING, db_column='idCalle')

    class Meta:
        managed = False
        db_table = 'sensor'


class Medicion(models.Model):
    id_medicion = models.AutoField(db_column='idMedicion', primary_key=True)
    creado = models.DateTimeField(auto_now_add=True)
    nivel_agua = models.DecimalField(db_column='nivelAgua', max_digits=5, decimal_places=2, blank=True, null=True)  # noqa
    id_sensor = models.ForeignKey('Sensor', models.DO_NOTHING, db_column='idSensor')  # noqa

    class Meta:
        managed = False
        db_table = 'medicion'


class Destinatario(models.Model):
    email = models.CharField(primary_key=True, max_length=45)
    creado = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=45, blank=True, null=True)
    apellido = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'destinatario'
