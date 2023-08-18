from django.urls import path
from . import views
from .views import reporteList, reporteDetail


urlpatterns = [
    path('', views.reportes, name='reportes'),
    path('nuevo/', views.nuevo_reporte, name='nuevo_reporte'),
    path('modificar/<int:id_reporte>/', views.modificar_reporte, name='modificar_reporte'),
    path('eliminar/<int:id_reporte>/', views.eliminar_reporte, name='eliminar_reporte'),
    path('generar_qr/<int:id_reporte>/', views.generar_qr, name='generar_qr'),
    path('imprimir_qr/<int:id_reporte>/<str:formato>/', views.imprimir_qr, name='imprimir_qr'),
    path('duplicar_reportes/', views.duplicar_reportes, name='duplicar_reportes'),
    path('eliminar_reportes/', views.eliminar_reporte_multiple, name='eliminar_reporte_multiple'),
    path('api/reportes/', reporteList.as_view(), name='reportes_api'),
    path('api/reportes/<int:id_reporte>/', reporteDetail.as_view(), name='reporte_detail_api'),

]