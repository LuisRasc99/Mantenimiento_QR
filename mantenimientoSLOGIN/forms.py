from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import Usuario, DatosAdministrador, DatosTecnico

class RegistroForm(UserCreationForm):
    ROLES = [
        ('administrador', 'Administrador'),
        ('tecnico', 'Técnico'),
    ]

    rol = forms.ChoiceField(choices=ROLES)
    

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2', 'rol']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Correo electronico/Usuario')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            usuario = authenticate(username=username, password=password)
            if usuario is None:
                try:
                    usuario = Usuario.objects.get(email=username)
                    usuario = authenticate(request=self.request, username=Usuario.email, password=password)
                except Usuario.DoesNotExist:
                    raise forms.ValidationError('Las credenciales ingresadas son incorrectas.')
        return self.cleaned_data
    
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nombre', 'apellido_materno', 'apellido_paterno', 'calle','numero_calle', 'colonia', 'ciudad', 'codigo_postal', 'telefono')
        labels = {
            'apellido_materno': 'Apellido Materno',
            'apellido_paterno': 'Apellido Paterno',
            'numero_calle': 'Numero de calle',
        }


