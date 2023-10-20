from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.utils import timezone

class Usuarios(AbstractUser):
    username = models.CharField(max_length=80, unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)
    rol = models.CharField(max_length=20)

    class Meta:
        db_table = 'Usuarios'


class Tecnico(SuperUsuario):
    
    nombre = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    calle = models.CharField(max_length=100)
    numero_calle = models.CharField(max_length=100)
    colonia = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)
    telefono = models.CharField(max_length=15)
    celular = models.CharField(max_length=15)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    foto_tecnico = models.ImageField(upload_to='tecnicos/', blank=True, null=True)
    
    class Meta:
        db_table = 'tecnico'





class DatosAdministrador(models.Model):
    user = models.OneToOneField(Administrador, on_delete=models.CASCADE)
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
    user = models.OneToOneField(Tecnico, on_delete=models.CASCADE)
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