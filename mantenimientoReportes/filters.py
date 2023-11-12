import django_filters
from .models import Inventario

class InventarioFilter(django_filters.FilterSet):
    nombre_partes = django_filters.CharFilter(lookup_expr='icontains', label='Nombre de la Parte')
    numero_partes = django_filters.CharFilter(lookup_expr='icontains', label='Número de la Parte')

    class Meta:
        model = Inventario
        fields = ['nombre_partes', 'numero_partes']
