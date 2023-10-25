from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.inicio, name= 'inicio'),

    path('registrar/', views.registrar, name= 'registrar'),
    path('registrar/PerfilUsuario/', views.PerfilUsuario, name= 'PerfilUsuario'),
    #path('registrar/DatosTecnico/', views.DatosTecnico, name= 'DatosTecnico'),

    path('isesion/', views.isesion, name= 'isesion'),

    path('logout/', views.csesion, name= 'logout'),
    
    path('modificar_datos/', views.modificar_datos, name='modificar_datos'),
]
