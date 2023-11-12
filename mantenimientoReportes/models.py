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

def maquina_image_path(instance, filename):
    # Generar la ruta de almacenamiento para la imagen de la máquina
    return f'maquina_img/{filename}'

def filtro_image_path(instance, filename):
    # Generar la ruta de almacenamiento para la imagen del filtro
    return f'filtros_img/{filename}'

class Maquina(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_maquina = models.TextField(max_length=100)
    marca = models.TextField(max_length=100)
    modelo = models.TextField(max_length=100)
    contador_horas = models.DecimalField(max_digits=10, decimal_places=2)
    foto_maquina = models.ImageField(upload_to='maquinas/', null=True, blank=True)

    def __str__(self):
        return self.nombre_maquina


class Partes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_partes = models.TextField(max_length=100)
    numero_partes = models.TextField(max_length=20)
    cantidad_partes = models.IntegerField()
    costo_aproximado = models.DecimalField(max_digits=10, decimal_places=2)
    horas_uso = models.DecimalField(max_digits=10, decimal_places=2)
    foto_partes = models.ImageField(upload_to='partes/', null=True, blank=True)
    maquinas = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='partes')
    inventarios = models.ForeignKey('Inventario', on_delete=models.CASCADE, related_name='partes', null=True, blank=True)

    def __str__(self):
        return self.nombre_partes

class Inventario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_partes = models.TextField(max_length=100)
    numero_partes = models.TextField(max_length=20)
    cantidad_partes = models.IntegerField(default=0)
    costo_aproximado = models.DecimalField(max_digits=10, decimal_places=2)
    horas_uso = models.DecimalField(max_digits=10, decimal_places=2)
    foto_partes = models.ImageField(upload_to='partes/', null=True, blank=True)
    

    def __str__(self):
        return self.nombre_partes
    
    def obtener_datos_maquina(self):
        # Accede a los datos de la máquina a través de la relación inversa con Partes
        if self.partes.exists():
            # Utiliza first() para obtener la primera parte asociada
            parte_asociada = self.partes.first()
            maquina_asociada = parte_asociada.maquinas
            return {
                'nombre_maquina': maquina_asociada.nombre_maquina,
                'marca': maquina_asociada.marca,
                'modelo': maquina_asociada.modelo,
                'contador_horas': maquina_asociada.contador_horas,
                'foto_maquina': maquina_asociada.foto_maquina.url if maquina_asociada.foto_maquina else None,
            }
        else:
            return None




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
    foto = models.ImageField(upload_to=maquina_image_path, blank=True, null=True)
    foto_filtro = models.ImageField(upload_to=filtro_image_path, blank=True, null=True)
    def __str__(self):
        return f"{self.nombre_maquina}"

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
    # Actualizar las imágenes del reporte al guardar si se han cambiado las imágenes
    if instance.id_reporte:
        try:
            reporte = Reportes.objects.get(id_reporte=instance.id_reporte)

            # Verificar y eliminar la imagen anterior de la máquina
            if reporte.foto != instance.foto:
                if reporte.foto:
                    if os.path.isfile(reporte.foto.path):
                        os.remove(reporte.foto.path)

            # Verificar y eliminar la imagen anterior del filtro
            if reporte.foto_filtro != instance.foto_filtro:
                if reporte.foto_filtro:
                    if os.path.isfile(reporte.foto_filtro.path):
                        os.remove(reporte.foto_filtro.path)

        except Reportes.DoesNotExist:
            pass
        
@receiver(models.signals.pre_delete, sender=Reportes)
def eliminar_fotos(sender, instance, **kwargs):
    for field_name in ['foto', 'foto_filtro']:
        foto_field = getattr(instance, field_name)
        if foto_field:
            foto_path = foto_field.path
            if os.path.isfile(foto_path):
                os.remove(foto_path)

class Historial(models.Model):
    reporte = models.ForeignKey(Reportes, on_delete=models.CASCADE)
    usuario_modificacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tipo_modificacion = models.CharField(max_length=20)  # Puedes usar choices para definir opciones
    fecha_modificacion = models.DateTimeField(auto_now_add=True)
    nombre_maquina_anterior = models.CharField(max_length=100, null=True, blank=True)
    descripcion_anterior = models.TextField(null=True, blank=True)
    numero_parte_anterior = models.CharField(max_length=100, null=True, blank=True)
    piezas_anterior = models.IntegerField(null=True, blank=True)
    costo_anterior = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    horas_anterior = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_reemplazo_anterior = models.DateField(null=True, blank=True)
    qr_anterior = models.ImageField(upload_to='qr/historial', blank=True, null=True)

    def __str__(self):
        return f"Historial de modificación para {self.reporte.nombre_maquina}"
    
    def generar_qr_anterior(self):
        data = f"Nombre de máquina anterior: {self.nombre_maquina_anterior}\nDescripción anterior: {self.descripcion_anterior}\nNúmero de parte anterior: {self.numero_parte_anterior}\nPiezas anteriores: {self.piezas_anterior}\nCosto anterior: {self.costo_anterior}\nHoras anteriores: {self.horas_anterior}\nFecha de reemplazo anterior: {self.fecha_reemplazo_anterior}\nFecha de modificación: {self.fecha_modificacion}"
        
        qr_img = qrcode.make(data)
        qr_bytes = BytesIO()
        qr_img.save(qr_bytes, format='PNG')

        # Utiliza default_storage.save() para guardar el archivo en la ubicación correcta
        qr_filename = f'qr_anterior_{self.id}.png'
        qr_path = os.path.join('qr', 'historial', qr_filename)
        default_storage.save(qr_path, File(qr_bytes), max_length=None)

        self.qr_anterior.name = qr_path  # Actualiza el nombre del campo en el modelo
        self.save(update_fields=['qr_anterior'])  # Guarda el registro actualizado en la base de datos

    def eliminar_archivos(self):
        for field_name in ['foto_anterior', 'foto_filtro_anterior', 'qr_anterior']:
            image_field = getattr(self, field_name)
            if image_field:
                if default_storage.exists(image_field.name):
                    default_storage.delete(image_field.name)

    def delete(self, *args, **kwargs):
        self.eliminar_archivos()
        super(Historial, self).delete(*args, **kwargs)

