import qrcode
from django import forms
from .models import Maquina, Inventario
from django.core.files import File
from io import BytesIO

class MaquinaForm(forms.ModelForm):
    class Meta:
        model = Maquina
        fields = ['maquina', 'marca', 'modelo', 'horas_maquina', 'foto_maquina']

