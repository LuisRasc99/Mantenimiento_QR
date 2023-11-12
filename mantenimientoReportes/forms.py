import qrcode
from django import forms
from .models import Maquina, Partes, Reportes, Inventario
from django.core.files import File
from io import BytesIO
import django_filters


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
        fields = ['nombre_maquina', 'marca', 'modelo', 'contador_horas', 'foto_maquina']

    def __init__(self, *args, **kwargs):
        super(MaquinaForm, self).__init__(*args, **kwargs)
        self.fields['foto_maquina'].required = True

class  InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['nombre_partes', 'numero_partes','cantidad_partes','costo_aproximado', 'horas_uso', 'foto_partes']

    def __init__(self, *args, **kwargs):
        super(InventarioForm, self).__init__(*args, **kwargs)
        self.fields['foto_partes'].required = True

    def clean_foto_partes(self):
        foto_partes = self.cleaned_data.get('foto_partes')
        
        # Verifica si ya existe una parte con la misma imagen
        parte_existente = Partes.objects.filter(foto_partes=foto_partes).first()

        if parte_existente:
            # Si existe, devuelve la instancia de la parte existente
            return parte_existente.foto_partes

        return foto_partes

class  PartesForm(forms.ModelForm):
    class Meta:
        model = Partes
        fields = ['nombre_partes', 'numero_partes','cantidad_partes','costo_aproximado', 'horas_uso', 'foto_partes']

    def __init__(self, *args, **kwargs):
        super(PartesForm, self).__init__(*args, **kwargs)
        self.fields['foto_partes'].required = True

    def clean_foto_partes(self):
        foto_partes = self.cleaned_data.get('foto_partes')
        
        # Verifica si ya existe una parte con la misma imagen
        parte_existente = Partes.objects.filter(foto_partes=foto_partes).first()

        if parte_existente:
            # Si existe, devuelve la instancia de la parte existente
            return parte_existente.foto_partes

        return foto_partes

