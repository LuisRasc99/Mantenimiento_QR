import qrcode
from django import forms
from .models import CatalogoPartes, Maquina, MovimientoInventario
from django.core.files import File
from io import BytesIO

class MaquinaForm(forms.ModelForm):
    class Meta:
        model = Maquina
        fields = ['maquina', 'marca', 'modelo', 'horas_maquina', 'foto_maquina']

class CatalogoPartesForm(forms.ModelForm):
    class Meta:
        model = CatalogoPartes
        fields = ['nombre_partes', 'numero_partes', 'horas_vida', 'foto_partes', 'costo_aproximado']
        
class InventarioEntradaForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['partes', 'piezas_entrada']
        

class InventarioSalidaForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['maquinas', 'partes', 'piezas_salida', 'new_horas_maquina']