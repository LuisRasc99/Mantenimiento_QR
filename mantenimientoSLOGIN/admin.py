from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from mantenimientoSLOGIN.forms import UsuarioForm
from .models import Usuario, DatosUsuario
from .forms import CustomUserCreationForm

class UsuarioAdminForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'

    def clean_tipo_usuario(self):
        tipo_usuario = self.cleaned_data.get('tipo_usuario')
        if tipo_usuario == 'superusuario':
            self.instance.is_staff = True
            self.instance.is_superuser = True
        else:
            self.instance.is_staff = False
            self.instance.is_superuser = False
        return tipo_usuario

    def save(self, commit=True):
        # Ajustar los valores de is_staff e is_superuser
        tipo_usuario = self.cleaned_data.get('tipo_usuario')
        if tipo_usuario in ['administrador', 'tecnico']:
            self.instance.is_staff = False
            self.instance.is_superuser = False
        elif tipo_usuario == 'superusuario':
            self.instance.is_staff = True
            self.instance.is_superuser = True

        # Llamar al método save del formulario base
        return super().save(commit)
    
class CustomUsuarioAdmin(UserAdmin):
    add_form = CustomUserCreationForm  # Usa el nuevo formulario para la creación
    form = UsuarioAdminForm
    model = Usuario
    list_display = ['username', 'email', 'tipo_usuario', 'is_staff']

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permisos', {'fields': ('tipo_usuario', 'is_active', 'is_staff', 'is_superuser')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'tipo_usuario', 'password1', 'password2'),
        }),
    )

class DatosUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'nombre', 'apellido_pat', 'apellido_mat', 'calle', 'numero_calle', 'colonia', 'ciudad', 'cp', 'telefono')
    search_fields = ('nombre', 'apellido_pat', 'apellido_mat', 'calle', 'ciudad', 'cp', 'telefono')
    list_filter = ('user',)  # Puedes agregar filtros según tus necesidades

admin.site.register(Usuario, CustomUsuarioAdmin)  # Registrar el modelo una s
admin.site.register(DatosUsuario, DatosUsuarioAdmin)
 