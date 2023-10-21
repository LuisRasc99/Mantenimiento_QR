from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.utils import timezone

class Usuarios(AbstractUser):
    # Otros campos de usuario

    rol = models.CharField(max_length=20)

# Agregar related_name personalizado a las relaciones con Group y Permission
Usuarios.groups.field.remote_field.related_name = 'usuarios_groups'
Usuarios.user_permissions.field.remote_field.related_name = 'usuarios_user_permissions'

class DatosAdministrador(models.Model):
    # Define una relación uno a uno con Usuario y un filtro para el rol de administrador
    user = models.OneToOneField(Usuarios, on_delete=models.CASCADE, limit_choices_to={'rol': 'administrador'})
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
    foto_user = models.ImageField(upload_to='usuarios/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class DatosTecnico(models.Model):
    user = models.OneToOneField(Usuarios, on_delete=models.CASCADE, limit_choices_to={'rol': 'tecnico'})
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
    
    def __str__(self):
        return self.user.username