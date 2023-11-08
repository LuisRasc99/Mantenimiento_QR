import qrcode
from django import forms
from .models import Maquina, Reportes, Inventario
from django.core.files import File
from io import BytesIO


class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reportes
        exclude = ('qr', 'user', 'fecha_reporte')

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

class MaquinaForm(forms.ModelForm):
    class Meta:
        model = Maquina
        fields = ['nombre_maquina', 'marca', 'modelo', 'foto_maquina']

    def __init__(self, *args, **kwargs):
        super(MaquinaForm, self).__init__(*args, **kwargs)
        self.fields['foto_maquina'].required = True

class  InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['nombre_pieza', 'numero_pieza','cantidad_pieza','ultimo_costo', 'horas_uso', 'foto_pieza']

    def __init__(self, *args, **kwargs):
        super(InventarioForm, self).__init__(*args, **kwargs)
        self.fields['foto_pieza'].required = True

class  PartesForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['nombre_parte', 'numero_parte','cantidad_partes','ultimo_costo', 'horas_uso', 'foto_partes']

    def __init__(self, *args, **kwargs):
        super(InventarioForm, self).__init__(*args, **kwargs)
        self.fields['foto_partes'].required = True