from django.urls import path
from . import views
from .views import reporteList, reporteDetail


urlpatterns = [
    path('', views.reportes, name='reportes'),

    path('panel/', views.panel, name='panel'),
    path('panel/nueva_maquina', views.nueva_maquina, name='nueva_maquina'),
    path('panel/modificar_maquina/<int:maquina_id>/', views.modificar_maquina, name='modificar_maquina'),
    path('panel/eliminar_maquina/<int:maquina_id>/', views.eliminar_maquina, name='eliminar_maquina'),
    
    path('panel/inventario', views.inventario, name='inventario'),
    path('panel/inventario/nuevo', views.nuevo_inventario, name='nuevo_inventario'),
    path('panel/inventario/modificar/<int:inventario_id>/', views.modificar_inventario, name='modificar_inventario'),
    path('panel/inventario/eliminar/<int:inventario_id>/', views.eliminar_inventario, name='eliminar_inventario'),


]