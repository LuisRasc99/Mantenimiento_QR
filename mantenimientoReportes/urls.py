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

    path('panel/partes/<int:maquina_id>/', views.partes, name='partes'),
    path('panel/partes/nuevo/<int:maquina_id>/', views.nuevo_partes, name='nuevo_partes'),
    path('panel/partes/modificar/<int:partes_id>/', views.modificar_partes, name='modificar_partes'),
    path('panel/partes/eliminar/<int:partes_id>/', views.eliminar_partes, name='eliminar_partes'),

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

    path('api/reportes/', reporteList.as_view(), name='reportes_api'),
    path('api/reportes/<int:id_reporte>/', reporteDetail.as_view(), name='reporte_detail_api'),

]