from django.contrib.auth import get_user_model
from django.db import models
import qrcode
import os
from io import BytesIO
from django.core.files import File
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
import os
from decimal import Decimal
from django.core.files.storage import default_storage
User = get_user_model()

class Maquina(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    maquina = models.TextField(max_length=100)
    marca = models.TextField(max_length=100)
    modelo = models.TextField(max_length=100)
    horas_maquina = models.DecimalField(max_digits=10, decimal_places=2)
    nombre_maquina = models.TextField(max_length=100)
    foto_maquina = models.ImageField(upload_to='maquinas/', null=True, blank=True)
    foto_maquina = models.ImageField(upload_to='qr/', null=True, blank=True)
    partes = models.ForeignKey('CatalogoPartes', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_maquina

class CatalogoPartes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_partes = models.TextField(max_length=100)
    numero_partes = models.TextField(max_length=20)
    horas_vida = models.DecimalField(max_digits=10, decimal_places=2)
    foto_partes = models.ImageField(upload_to='partes/', null=True, blank=True)
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)

class MantenimientoPartes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_mantenimiento = models.DateField(auto_now_add=True)
    piezas_salida = models.IntegerField()
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    partes = models.ForeignKey(CatalogoPartes, on_delete=models.CASCADE)

class Inventario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_entrada = models.DateField(auto_now_add=True)
    piezas_entrada = models.IntegerField()
    costo_aproximado = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    partes = models.ForeignKey(CatalogoPartes, on_delete=models.CASCADE)
    mantenimiento = models.ForeignKey(MantenimientoPartes, on_delete=models.CASCADE)

    