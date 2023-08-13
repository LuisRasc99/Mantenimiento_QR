from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import DatosUsuario


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Correo electronico/Usuario')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                try:
                    user = User.objects.get(email=username)
                    user = authenticate(request=self.request, username=user.email, password=password)
                except User.DoesNotExist:
                    raise forms.ValidationError('Las credenciales ingresadas son incorrectas.')
        return self.cleaned_data
    
class DatosUsuarioForm(forms.ModelForm):
    class Meta:
        model = DatosUsuario
        fields = ('nombre', 'apellido_materno', 'apellido_paterno', 'calle','numero_calle', 'colonia', 'ciudad', 'codigo_postal', 'telefono')
        labels = {
            'apellido_materno': 'Apellido Materno',
            'apellido_paterno': 'Apellido Paterno',
            'numero_calle': 'Numero de calle',
        }