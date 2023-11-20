from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, DatosUsuario

class UsuarioAdminForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'

    def save(self, commit=True):
        # Establecer is_staff e is_superuser según el tipo de usuario seleccionado
        tipo_usuario = self.cleaned_data.get('tipo_usuario')
        if tipo_usuario == 'superusuario':
            self.instance.is_staff = True
            self.instance.is_superuser = True
        elif tipo_usuario == 'administrador':
            self.instance.is_staff = True
            self.instance.is_superuser = False

        return super().save(commit)

class CustomUsuarioAdmin(UserAdmin):
    add_form = UsuarioAdminForm
    form = UsuarioAdminForm
    model = Usuario
    list_display = ['username', 'email', 'tipo_usuario', 'is_staff']

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permisos', {'fields': ('tipo_usuario', 'is_active', 'is_staff', 'is_superuser')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Usuario)
class CustomUsuarioAdmin(UserAdmin):
    add_form = UsuarioAdminForm
    form = UsuarioAdminForm
    model = Usuario
    list_display = ['username', 'email', 'tipo_usuario', 'is_staff']

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password1', 'password2')}),
        ('Permisos', {'fields': ('tipo_usuario', 'is_active', 'is_staff', 'is_superuser')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(DatosUsuario)
class DatosUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'nombre', 'apellido_pat', 'apellido_mat', 'ciudad', 'cp', 'telefono']
