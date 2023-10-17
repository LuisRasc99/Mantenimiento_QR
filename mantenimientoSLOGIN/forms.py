from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import DatosAdministrador, DatosTecnico, Administrador, Tecnico

class AdministradorForm(forms.ModelForm):
    class Meta:
        model = Administrador
        exclude = ['fecha_registro', 'foto_user']

class DatosAdministradorForm(forms.ModelForm):
    class Meta:
        model = DatosAdministrador
        exclude = ['fecha_registro', 'foto_tecnico']

class DatosTecnicoForm(forms.ModelForm):
    class Meta:
        model = DatosTecnico
        exclude = ['fecha_registro']



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')