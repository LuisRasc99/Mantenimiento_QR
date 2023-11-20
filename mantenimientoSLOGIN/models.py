from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class Usuario(AbstractUser):
    TIPO_USUARIO_OPCIONES = [
        ('superusuario', 'Superusuario'),
        ('administrador', 'Administrador'),
        ('tecnico', 'Técnico'),
    ]
    tipo_usuario = models.CharField(max_length=50, choices=TIPO_USUARIO_OPCIONES, default='Administrador')
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class DatosUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='datos_usuario')
    nombre = models.CharField(max_length=255)
    apellido_pat = models.CharField(max_length=255)
    apellido_mat = models.CharField(max_length=255)
    calle = models.CharField(max_length=255)
    numero_calle = models.IntegerField(default=0, null=True)  # Cambiado a 0
    colonia = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=255)
    cp = models.IntegerField(default=0, null=True)  # Cambiado a 0
    telefono = models.IntegerField(default=0, null=True)  # Cambiado a 0
    fecha_registro = models.DateTimeField(auto_now_add=True)