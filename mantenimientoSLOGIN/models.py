from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

ROL_CHOICES = [
    ('administrador', 'Administrador'),
    ('tecnico', 'Técnico'),
]

class AdministradorManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class TecnicoManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    
class Administrador(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='administrador')  # Campo para el rol

    # Otros campos personalizados según tus necesidades

    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = AdministradorManager()

    # Agrega related_name personalizados
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='administradores'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='administradores'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
class Tecnico(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='tecnico')
    # Agrega los campos personalizados específicos para el técnico aquí
    

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = TecnicoManager()

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='tecnicos'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='tecnicos'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'rol']

    def __str__(self):
        return self.username


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
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='usuario')  # Agregar el campo "rol"# Agregar el campo "rol"

    def __str__(self):
        return self.user.username
    
class DatosTecnicos(models.Model):
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
    foto_tecnico = models.ImageField(upload_to='tecnicos/', blank=True, null=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='tecnico')  # Agregar el campo "rol"

    def __str__(self):
        return self.user.username