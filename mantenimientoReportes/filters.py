import django_filters
from .models import CatalogoPartes, Inventario
from django.db.models import Q

class InventarioFilter(django_filters.FilterSet):
    nombre_partes = django_filters.CharFilter(lookup_expr='icontains', label='Nombre de la Parte')
    numero_partes = django_filters.CharFilter(lookup_expr='icontains', label='Número de la Parte')

    class Meta:
        model = Inventario
        fields = ['nombre_partes', 'numero_partes']

class CatalogoPartesFilter(django_filters.FilterSet):
    
    class Meta:
        model = CatalogoPartes
        fields = ['nombre_partes', 'numero_partes']