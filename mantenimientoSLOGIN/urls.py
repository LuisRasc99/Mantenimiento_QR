from django.urls import path
from . import views

urlpatterns = [
    path('', views.IniciarSesion, name='iniciar_sesion'),
    path('cerrar_sesion/', views.CerrarSesion, name='cerrar_sesion'),
    path('registrar/', views.Registrar, name='registrar'),
    path('datos_usuario/<int:user_id>/', views.DatosUsuario, name='datos_usuario'),

    path('tecnicos/', views.Tecnicos, name='tecnicos'),
    path('tecnicos/registrar/', views.RegistrarTecnicos, name='registrar_tecnico'),
    # Agrega otras URLs según sea necesario
]