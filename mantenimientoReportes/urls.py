from django.urls import path
from . import views


urlpatterns = [
    path('', views.reportes, name='reportes'),
    path('nuevo/', views.nuevo_reporte, name='nuevo_reporte'),
    path('modificar/<int:id_reporte>/', views.modificar_reporte, name='modificar_reporte'),
    path('eliminar/<int:id_reporte>/', views.eliminar_reporte, name='eliminar_reporte'),
    path('generar_qr/<int:id_reporte>/', views.generar_qr, name='generar_qr'),
    path('imprimir_qr/<int:id_reporte>/<str:formato>/', views.imprimir_qr, name='imprimir_qr'),
    path('duplicar_reportes/', views.duplicar_reportes, name='duplicar_reportes'),
    path('eliminar_reportes/', views.eliminar_reporte_multiple, name='eliminar_reporte_multiple'),
    path('reportes/<int:reporte_id>/historial/', views.historial_reportes, name='historial_reportes'),
    path('eliminar_historial/<int:id_historial>/', views.eliminar_historial, name='eliminar_historial'),
    path('imprimir_qr_anterior/<int:id_historial>/<str:formato>/', views.imprimir_qr_anterior, name='imprimir_qr_anterior'),

]