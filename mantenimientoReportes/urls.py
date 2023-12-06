from django.urls import path
from . import views


urlpatterns = [
    path('', views.panel, name='panel'),
    path('nueva_maquina/', views.nueva_maquina, name='nueva_maquina'), 
    path('modificar_maquina/<int:maquina_id>/', views.modificar_maquina, name='modificar_maquina'),
    path('eliminar_maquina/<int:maquina_id>/', views.eliminar_maquina, name='eliminar_maquina'),

    path('partes', views.partes, name='partes'), 
    path('partes/modificar_partes/<int:parte_id>/', views.modificar_partes, name='modificar_partes'),
    path('partes/eliminar_partes/<int:parte_id>/', views.eliminar_partes, name='eliminar_partes'),

    path('inventario_entrada/', views.inventario_entrada, name='inventario_entrada'),
    path('inventario_entrada/editar/<int:inventario_id>/', views.editar_inventario_entrada, name='editar_inventario_entrada'),
    path('inventario_entrada/eliminar/<int:inventario_id>/', views.eliminar_inventario_entrada, name='eliminar_inventario_entrada'),

    path('mantenimiento/', views.mantenimiento, name='mantenimiento'),
    path('mantenimiento/editar/<int:mantenimiento_id>/', views.editar_mantenimiento, name='editar_mantenimiento'),
    path('mantenimiento/eliminar/<int:mantenimiento_id>/', views.eliminar_mantenimiento, name='eliminar_mantenimiento'),

    path('almacen/', views.almacen, name='almacen'),
]