import qrcode
from django import forms
from .models import CatalogoPartes, MantenimientoPartes, Maquina, Inventario
from django.core.files import File
from io import BytesIO

class MaquinaForm(forms.ModelForm):
    class Meta:
        model = Maquina
        fields = ['maquina', 'marca', 'modelo', 'horas_maquina', 'foto_maquina']

class CatalogoPartesForm(forms.ModelForm):
    class Meta:
        model = CatalogoPartes
        fields = ['nombre_partes', 'numero_partes', 'horas_vida', 'foto_partes']

class MantenimientoPartesForm(forms.ModelForm):
    class Meta:
        model = MantenimientoPartes
        fields = ['maquina', 'partes', 'piezas_salida', 'hrs']

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['maquina', 'partes', 'piezas_entrada', 'costo_aproximado']
        exclude = ['cantidad_piezas', 'fecha_entrada']