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
User = get_user_model()

def reporte_image_path(instance, filename):
    # Generar la ruta de almacenamiento para la imagen del reporte
    return f'static/reportes_img/{filename}'

class Reportes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_reporte = models.AutoField(primary_key=True)
    nombre_maquina = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    numero_parte = models.CharField(max_length=100, null=True, blank=True)
    piezas = models.IntegerField(null=True, blank=True)
    costo = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    horas = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_reemplazo = models.DateField(null=True, blank=True)
    fecha_reporte = models.DateField(auto_now_add=True)
    qr = models.ImageField(upload_to='qr/', blank=True, null=True)
    foto = models.ImageField(upload_to=reporte_image_path, blank=True, null=True)
    def __str__(self):
        return f"{self.titulo} - {self.autor}"

    def generar_qr(self):
        data = f"Nombre de máquina: {self.nombre_maquina}\nDescripción: {self.descripcion}\nNúmero de parte: {self.numero_parte}\nPiezas: {self.piezas}\nCosto: {self.costo}\nHoras: {self.horas}\nFecha de reemplazo: {self.fecha_reemplazo}\nFecha de reporte: {self.fecha_reporte}"
        if self.qr:  # Verificar si hay un código QR existente
            self.qr.delete()  # Eliminar el código QR anterior
        qr_img = qrcode.make(str(data))
        qr_bytes = BytesIO()
        qr_img.save(qr_bytes, format='PNG')
        qr_file = File(qr_bytes, name=f'qr_{self.id_reporte}.png')
        self.qr.save(f'qr_{self.id_reporte}.png', qr_file)
        

@receiver(pre_delete, sender=Reportes)
def eliminar_qr(sender, instance, **kwargs):
    # Eliminar el archivo de código QR cuando se elimine el reporte
    if instance.qr:
        if os.path.isfile(instance.qr.path):
            os.remove(instance.qr.path)   

@receiver(pre_save, sender=Reportes)
def actualizar_imagen_reporte(sender, instance, **kwargs):
    # Actualizar la imagen del reporte al guardar si se ha cambiado la imagen
    if instance.id_reporte:
        try:
            reporte = Reportes.objects.get(id_reporte=instance.id_reporte)
            if reporte.foto != instance.foto:
                # Eliminar la imagen anterior del reporte
                if reporte.foto:
                    if os.path.isfile(reporte.foto.path):
                        os.remove(reporte.foto.path)
        except Reportes.DoesNotExist:
            pass
        
@receiver(models.signals.pre_delete, sender=Reportes)
def eliminar_foto(sender, instance, **kwargs):
    if instance.foto:
        # Obtener la ruta de la foto
        foto_path = instance.foto.path
        # Verificar si el archivo existe
        if os.path.isfile(foto_path):
            # Eliminar el archivo de la foto
            os.remove(foto_path)