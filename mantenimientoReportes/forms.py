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
        fields = ['nombre_partes', 'numero_partes', 'horas_vida', 'foto_partes', 'costo_aproximado']
        

class MantenimientoPartesForm(forms.ModelForm):
    class Meta:
        model = MantenimientoPartes
        fields = ['maquina', 'partes', 'inventario', 'piezas_salida', 'hrs']

    def clean_piezas_salida(self):
        piezas_salida = self.cleaned_data['piezas_salida']
        inventario = self.cleaned_data['inventario']

        if inventario and piezas_salida > inventario.total_piezas:
            raise forms.ValidationError(
                f"La cantidad de piezas de salida no puede ser mayor que el total disponible ({inventario.total_piezas})."
            )

        return piezas_salida

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['partes', 'piezas_entrada']
        exclude = ['cantidad_piezas', 'fecha_entrada','costo_total']