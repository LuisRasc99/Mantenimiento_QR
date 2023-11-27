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

    path('mantenimiento_partes/', views.mantenimiento_partes, name='mantenimiento_partes'),
    path('editar_mantenimiento/<int:mantenimiento_id>/', views.editar_mantenimiento, name='editar_mantenimiento'),

    path('inventario/', views.inventario, name='inventario'),
    path('editar_inventario/<int:inventario_id>/', views.editar_inventario, name='editar_inventario'),

]