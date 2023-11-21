from django.urls import path
from . import views


urlpatterns = [
    path('', views.panel, name='panel'),
    path('nueva_maquina/', views.nueva_maquina, name='nueva_maquina'), 
    path('modificar_maquina/<int:maquina_id>/', views.modificar_maquina, name='modificar_maquina'),
]