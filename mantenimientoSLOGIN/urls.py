from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [

    path('', views.inicio, name= 'inicio'),
    path('registrar/', views.registrar, name= 'registrar'),
    path('registrar/datos_administrador/', views.DatosAdministrador, name= 'DatosAdministrador'),
    path('registrar/datos_administrador/', views.DatosTecnico, name= 'DatosTecnico'),


    #path('isesion/', views.isesion, name= 'isesion'),
    #path('logout/', views.csesion, name= 'logout'),
    #path('modificar_datos/', views.modificar_datos, name='modificar_datos'),
    #path('api/inicio/', views.api_inicio, name='api_inicio'),
    #path('api/datos-usuario/', views.api_datos_usuario, name='api_datos_usuario'),
    #path('api/reportes/', ReporteList.as_view(), name='reportes_api'),
    #path('api/reportes/<int:id_reporte>/', ReporteDetail.as_view(), name='reporte_detail_api'),
    #path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    #path('registrar_tecnicos/', views.registrar_tecnicos, name='registrar_tecnicos'),
    #path('lista_tecnicos/', views.lista_tecnicos, name= 'lista_tecnicos'),

]
