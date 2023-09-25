from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class User(models.Model):
    email = models.EmailField(unique=True)

class DatosUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    calle = models.CharField(max_length=100)
    numero_calle = models.CharField(max_length=100)
    colonia = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)
    telefono = models.CharField(max_length=15)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    
def imagen_tecnico_path(instance, filename):
    # Generar la ruta de almacenamiento para la imagen del técnico
    return f'tecnicos/{instance.user.username}/{filename}'

class Tecnicos(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    calle = models.CharField(max_length=100)
    numero_calle = models.CharField(max_length=100)
    colonia = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)
    telefono = models.CharField(max_length=15)
    email_tecnico = models.EmailField(unique=True)
    foto_tecnico = models.ImageField(upload_to=imagen_tecnico_path, blank=True, null=True)  # Agrega el campo de imagen
    fecha_registro = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=128)