from django.urls import path
from . import views


urlpatterns = [
    path('', views.maquina, name='panel'),
    # Agrega otras URLs según sea necesario
]