import qrcode
from django import forms
from .models import Reportes
from django.core.files import File
from io import BytesIO


class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reportes
        exclude = ('qr', 'usuario', 'fecha_reporte')

    # Configurar los campos como no requeridos
    nombre_maquina = forms.CharField(required=False)
    descripcion = forms.CharField(required=False)
    numero_parte = forms.CharField(required=False)
    piezas = forms.IntegerField(required=False)
    costo = forms.DecimalField(required=False)
    horas = forms.DecimalField(required=False)
    fecha_reemplazo = forms.DateField(required=False)

class ReporteUpdateForm(forms.ModelForm):
    class Meta:
        model = Reportes
        fields = ['nombre_maquina', 'descripcion', 'numero_parte', 'piezas', 'costo', 'horas', 'fecha_reemplazo', 'foto', 'foto_filtro']

    costo = forms.DecimalField(required=False)
    horas = forms.DecimalField(required=False)    
    fecha_reemplazo = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))   
        