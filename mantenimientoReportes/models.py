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
from appmantenimiento import settings
from mantenimientoSLOGIN.models import Usuario 



class Maquina(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    maquina = models.TextField(max_length=100)
    marca = models.TextField(max_length=100)
    modelo = models.TextField(max_length=100)
    horas_maquina = models.DecimalField(max_digits=10, decimal_places=2)
    nombre_maquina = models.TextField(max_length=100, blank=True, editable=False)
    foto_maquina = models.ImageField(upload_to='maquinas/', null=True, blank=True)
    qr = models.ImageField(upload_to='qr/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Elimina la imagen anterior si ha cambiado
        if self.pk:
            maquina_db = Maquina.objects.get(pk=self.pk)
            if maquina_db.foto_maquina != self.foto_maquina:
                ruta_anterior = os.path.join(settings.MEDIA_ROOT, str(maquina_db.foto_maquina))
                if os.path.isfile(ruta_anterior):
                    os.remove(ruta_anterior)

        # Construir el nombre de la máquina antes de guardar
        self.nombre_maquina = f"{self.maquina} {self.marca} {self.modelo}"

        super().save(*args, **kwargs)

class CatalogoPartes(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre_partes = models.TextField(max_length=100)
    numero_partes = models.TextField(max_length=20)
    horas_vida = models.DecimalField(max_digits=10, decimal_places=2)
    costo_aproximado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    foto_partes = models.ImageField(upload_to='partes/', null=True, blank=True)
    maquinas = models.ManyToManyField(Maquina, related_name='partes')
    

    def save(self, *args, **kwargs):
        # Elimina la imagen anterior si ha cambiado
        if self.pk:
            parte_db = CatalogoPartes.objects.get(pk=self.pk)
            if parte_db.foto_partes != self.foto_partes:
                ruta_anterior = os.path.join(settings.MEDIA_ROOT, str(parte_db.foto_partes))
                if os.path.isfile(ruta_anterior):
                    os.remove(ruta_anterior)

        super(CatalogoPartes, self).save(*args, **kwargs)

class MantenimientoPartes(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_mantenimiento = models.DateField(auto_now_add=True)
    piezas_salida = models.IntegerField(default=0)
    hrs = models.DecimalField(max_digits=10, decimal_places=2)
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='mantenimientos')
    partes = models.ForeignKey(CatalogoPartes, on_delete=models.CASCADE,)
    inventario = models.ForeignKey('Inventario', on_delete=models.CASCADE, null=True, blank=True, related_name='mantenimiento_inventario')
    
class Inventario(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    partes = models.ForeignKey(CatalogoPartes, on_delete=models.CASCADE)
    mantenimiento = models.OneToOneField(MantenimientoPartes, on_delete=models.CASCADE, null=True, blank=True, related_name='inventario_mantenimiento')
    piezas_entrada = models.PositiveIntegerField()
    fecha_entrada = models.DateField(auto_now_add=True)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_piezas = models.IntegerField(default=0)



