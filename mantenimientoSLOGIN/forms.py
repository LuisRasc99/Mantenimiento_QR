from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import DatosAdministrador,Administrador, DatosTecnicos



class CustomUserCreationForm(UserCreationForm):
    # Agregar un campo para seleccionar el rol
    ROL_CHOICES = [
        ('usuario', 'Usuario'),
        ('tecnico', 'Técnico'),
    ]
    
    class Meta:
        model = Administrador
        fields = ['username', 'email', 'password1', 'password2', 'rol']


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Correo electrónico/Usuario')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                try:
                    user = Administrador.objects.get(email=username)
                    user = authenticate(request=self.request, username=user.email, password=password)
                except Administrador.DoesNotExist:
                    raise forms.ValidationError('Las credenciales ingresadas son incorrectas.')
        return self.cleaned_data

class DatosAdministradorForm(forms.ModelForm):
    foto_user = forms.ImageField(label='Foto de Usuario', required=False)

    class Meta:
        model = DatosAdministrador
        fields = ('nombre', 'apellido_materno', 'apellido_paterno', 'calle', 'numero_calle', 'colonia', 'ciudad', 'codigo_postal', 'telefono')
        labels = {
            'apellido_materno': 'Apellido Materno',
            'apellido_paterno': 'Apellido Paterno',
            'numero_calle': 'Número de calle',
        }

class TecnicosForm(forms.ModelForm):
    foto_tecnico = forms.ImageField(label='Foto de Técnico', required=False)  # Agrega 'foto_tecnico' al formulario

    class Meta:
        model = DatosTecnicos
        exclude = ['fecha_registro', 'user']
