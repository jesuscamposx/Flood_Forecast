# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Alcaldia(models.Model):
    idalcaldia = models.AutoField(db_column='idAlcaldia', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)
    latitud = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True)
    longitud = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alcaldia'


class Calle(models.Model):
    idcalle = models.AutoField(db_column='idCalle', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=120)
    latitud = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True)
    longitud = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True)
    intensidad = models.IntegerField(blank=True, null=True)
    idmaps = models.CharField(db_column='idMaps', max_length=50, blank=True, null=True)  # Field name made lowercase.
    idcolonia = models.ForeignKey('Colonia', models.DO_NOTHING, db_column='idColonia')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'calle'


class Colonia(models.Model):
    idcolonia = models.AutoField(db_column='idColonia', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)
    latitud = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True)
    longitud = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True)
    idalcaldia = models.ForeignKey(Alcaldia, models.DO_NOTHING, db_column='idAlcaldia')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'colonia'


class Condicion(models.Model):
    idcondicion = models.AutoField(db_column='idCondicion', primary_key=True)  # Field name made lowercase.
    fecha = models.DateField()
    idcolonia = models.ForeignKey(Colonia, models.DO_NOTHING, db_column='idColonia')  # Field name made lowercase.
    precipitacion = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    tempmin = models.DecimalField(db_column='tempMin', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    tempmax = models.DecimalField(db_column='tempMax', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    inundacion = models.IntegerField(blank=True, null=True)
    creado = models.DateTimeField()
    actualizado = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'condicion'


class Destinatario(models.Model):
    email = models.CharField(primary_key=True, max_length=45)
    creado = models.DateTimeField()
    nombre = models.CharField(max_length=45, blank=True, null=True)
    apellido = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'destinatario'


class Medicion(models.Model):
    idmedicion = models.AutoField(db_column='idMedicion', primary_key=True)  # Field name made lowercase.
    creado = models.DateTimeField()
    nivelagua = models.DecimalField(db_column='nivelAgua', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    idsensor = models.ForeignKey('Sensor', models.DO_NOTHING, db_column='idSensor')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'medicion'


class Sensor(models.Model):
    idsensor = models.AutoField(db_column='idSensor', primary_key=True)  # Field name made lowercase.
    activado = models.IntegerField()
    latitud = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True)
    longitud = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True)
    idcalle = models.ForeignKey(Calle, models.DO_NOTHING, db_column='idCalle')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sensor'
