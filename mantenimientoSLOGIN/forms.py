from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import DatosUsuario, Usuario

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2', 'tipo_usuario')
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
            'tipo_usuario': 'Tipo de usuario',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.tipo_usuario == 'administrador':
            self.fields.pop('tipo_usuario')

class DatosUsuarioForm(forms.ModelForm):
    class Meta:
        model = DatosUsuario
        fields = ('nombre', 'apellido_pat', 'apellido_mat', 'calle', 'numero_calle', 'colonia', 'ciudad', 'cp', 'telefono')
        labels = {
            'nombre': 'Nombre',
            'apellido_pat': 'Apellido Paterno',
            'apellido_mat': 'Apellido Materno',
            'calle': 'Calle',
            'numero_calle': 'Número de Calle',
            'colonia': 'Colonia',
            'ciudad': 'Ciudad',
            'cp': 'Código Postal',
            'telefono': 'Teléfono',
        }

