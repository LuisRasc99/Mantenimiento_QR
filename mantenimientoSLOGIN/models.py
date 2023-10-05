from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Define las opciones de rol
ROL_CHOICES = [
    ('administrador', 'Administrador'),
    ('tecnico', 'Técnico'),
]

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
    foto_user = models.ImageField(upload_to='administradores/', blank=True, null=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='administrador')  # Agregar el campo "rol"

    def __str__(self):
        return self.user.username
    
class DatosTecnicos(models.Model):
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
    foto_tecnico = models.ImageField(upload_to='tecnicos/', blank=True, null=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='tecnico')  # Agregar el campo "rol"

    def __str__(self):
        return self.user.username