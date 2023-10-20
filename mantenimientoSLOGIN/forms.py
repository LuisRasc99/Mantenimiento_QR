from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import DatosAdministrador, DatosTecnico, Administrador, Tecnico, Usuarios

class RegistroFormulario(UserCreationForm):
    ROLES = [
        ('administrador', 'Administrador'),
        ('tecnico', 'Técnico'),
    ]

    rol = forms.ChoiceField(choices=ROLES)

    class Meta:
        model = Usuarios
        fields = ['username', 'email', 'password1', 'password2', 'rol']

class AdministradorForm(UserCreationForm):
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Administrador
        fields = ['username','email', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2

class TecnicoForm(UserCreationForm):
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Tecnico
        fields = ['username','email', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2

class DatosAdministradorForm(forms.ModelForm):
    class Meta:
        model = DatosAdministrador
        exclude = ['fecha_registro']

class DatosTecnicoForm(forms.ModelForm):
    class Meta:
        model = DatosTecnico
        exclude = ['fecha_registro']



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')