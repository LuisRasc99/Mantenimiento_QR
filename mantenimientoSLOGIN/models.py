from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

#--------------------------------USUARIO------------------------------------------------
class Usuario(AbstractUser):
    username = models.CharField(max_length=80, unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True)
    rol = models.CharField(max_length=20) 
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
    foto_administrador = models.ImageField(upload_to='administrador/', blank=True, null=True)
    
Usuario.groups.field.remote_field.related_name = 'usuarios_groups'
Usuario.user_permissions.field.remote_field.related_name = 'usuarios_user_permissions'

class DatosAdministrador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='administrador')
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
    foto_administrador = models.ImageField(upload_to='administrador/', blank=True, null=True)

    def __str__(self):
        return self.usuario.username
    
class DatosTecnico(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='tecnico')
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
    foto_administrador = models.ImageField(upload_to='tecnico/', blank=True, null=True)

    def __str__(self):
        return self.usuario.username
    
    
