import qrcode
from django import forms
from .models import Maquina, Partes, Reportes, Inventario
from django.core.files import File
from io import BytesIO
import django_filters  

class MaquinaForm(forms.ModelForm):
    class Meta:
        model = Maquina
        fields = ['nombre_maquina', 'marca', 'modelo', 'contador_horas', 'foto_maquina']

    def __init__(self, *args, **kwargs):
        super(MaquinaForm, self).__init__(*args, **kwargs)
        self.fields['foto_maquina'].required = True

class  InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['nombre_partes', 'numero_partes','cantidad_partes','costo_aproximado', 'horas_uso', 'foto_partes']

