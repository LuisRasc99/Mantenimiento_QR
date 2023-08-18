from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReporteForm, ReporteUpdateForm
from .models import Reportes
from django.contrib import messages
import qrcode
import os
from io import BytesIO
from django.core.files import File
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReporteSerializer
from uuid import uuid4
import shutil
import uuid
from django.db.models import Q


def nuevo_reporte(request):
    if request.method == 'POST':
        form = ReporteForm(request.POST, request.FILES)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.user = request.user  # Llenamos automáticamente el campo 'user' con el usuario actual
            reporte.save()
            reporte.generar_qr()
            return redirect('reportes')
    else:
        form = ReporteForm()
    return render(request, 'nuevo_reporte.html', {'form': form})


@login_required
def reportes(request):
    user = request.user
    reportes = Reportes.objects.filter(user=user)

    # Obtener el valor del parámetro GET 'search'
    search_query = request.GET.get('search')

    # Aplicar el filtro si hay un valor de búsqueda
    if search_query:
        reportes = reportes.filter(Q(nombre_maquina__icontains=search_query) | Q(descripcion__icontains=search_query))

    return render(request, 'reportes.html', {'reportes': reportes})

@login_required
def modificar_reporte(request, id_reporte):
    reporte = Reportes.objects.get(id_reporte=id_reporte)
    if request.method == 'POST':
        form = ReporteUpdateForm(request.POST, request.FILES, instance=reporte)
        if form.is_valid():
            if not form.cleaned_data['fecha_reemplazo']:
                form.cleaned_data['fecha_reemplazo'] = reporte.fecha_reemplazo
            reporte = form.save()
            reporte.generar_qr()
            return redirect('reportes')
    else:
        form = ReporteUpdateForm(instance=reporte)
    return render(request, 'modificar_reporte.html', {'form': form, 'reporte': reporte})

@login_required
def eliminar_reporte(request, id_reporte):
    reporte = Reportes.objects.get(id_reporte=id_reporte)
    if request.method == 'POST':
        eliminar_archivos_duplicados(reporte)
        eliminar_carpeta_duplicados(reporte.foto)
        eliminar_carpeta_duplicados(reporte.foto_filtro)
        reporte.delete()
        messages.success(request, 'El reporte ha sido eliminado exitosamente.')
        return redirect('reportes')
    return render(request, 'eliminar_reporte.html', {'reporte': reporte})

@login_required
def eliminar_reporte_multiple(request):
    if request.method == 'GET':
        reportes_ids = request.GET.get('ids', '').split(',')
        reportes_seleccionados = Reportes.objects.filter(id_reporte__in=reportes_ids)
        
        # Elimina los reportes seleccionados, sus archivos asociados y carpetas duplicadas
        for reporte in reportes_seleccionados:
            eliminar_archivos_duplicados(reporte)
            eliminar_carpeta_duplicados(reporte.foto)
            eliminar_carpeta_duplicados(reporte.foto_filtro)
            reporte.delete()

        messages.success(request, 'Los reportes seleccionados han sido eliminados exitosamente.')
        return redirect('reportes')

    return render(request, 'eliminar_reporte_multiple.html')

def eliminar_archivos_duplicados(reporte):
    if reporte.qr:
        if os.path.isfile(reporte.qr.path):
            os.remove(reporte.qr.path)

def eliminar_carpeta_duplicados(original_file):
    if original_file:
        original_path = original_file.path
        file_directory = os.path.dirname(original_path)
        duplicates_directory = os.path.join(file_directory, 'duplicates')
        try:
            shutil.rmtree(duplicates_directory)
        except Exception as e:
            print("Error deleting duplicates folder:", e) # Actualiza el nombre del template si es necesario

def duplicar_reportes(request):
    if request.method == 'GET':
        reportes_ids = request.GET.get('ids', '').split(',')
        reportes_seleccionados = Reportes.objects.filter(id_reporte__in=reportes_ids)
        
        # Duplica los reportes seleccionados y guárdalos en la base de datos
        for reporte_original in reportes_seleccionados:
            reporte_duplicado = Reportes.objects.get(pk=reporte_original.pk)  # Obtiene una nueva instancia del reporte original
            reporte_duplicado.pk = None  # Asigna un nuevo ID para crear una copia
            reporte_duplicado.qr = duplicate_file(reporte_original.qr)  # Duplica el archivo QR
            reporte_duplicado.foto = duplicate_file(reporte_original.foto)  # Duplica la imagen "foto"
            reporte_duplicado.foto_filtro = duplicate_file(reporte_original.foto_filtro)  # Duplica la imagen "foto_filtro"
            reporte_duplicado.save()

        return redirect('reportes')

def duplicate_file(original_file):
    if original_file:
        original_path = original_file.path
        file_extension = os.path.splitext(original_path)[-1]
        file_directory = os.path.dirname(original_path)
        new_filename = f'{uuid.uuid4()}{file_extension}'
        new_file_path = os.path.join(file_directory, 'duplicates', new_filename)
        
        try:
            os.makedirs(os.path.join(file_directory, 'duplicates'), exist_ok=True)
            shutil.copy(original_path, new_file_path)
        except IOError as e:
            print("Error copying file:", e)
            return None
        
        return new_file_path


def get_new_qr_path(original_path):
    original_basename = os.path.basename(original_path)
    original_dirname = os.path.dirname(original_path)
    new_basename = f"copy_{original_basename}"
    new_path = os.path.join(original_dirname, "qr", new_basename)  # Cambia la ruta para reflejar la carpeta "qr"
    return new_path

@login_required
def generar_qr(request, id_reporte):
    reporte = Reportes.objects.get(id_reporte=id_reporte)
    data = f"Nombre de máquina: {reporte.nombre_maquina}\nDescripción: {reporte.descripcion}\nNúmero de parte: {reporte.numero_parte}\nPiezas: {reporte.piezas}\nCosto: {reporte.costo}\nHoras: {reporte.horas}\nFecha de reemplazo: {reporte.fecha_reemplazo()}\nFecha de reporte: {reporte.fecha_reporte}"
    qr_img = qrcode.make(data)
    qr_bytes = BytesIO()
    qr_img.save(qr_bytes, format='PNG')
    qr_file = File(qr_bytes, name=f'qr_{reporte.id_reporte}.png')
    reporte.qr.save(f'qr_{reporte.id_reporte}.png', qr_file)
    reporte.save()
    return redirect('reporte')


from django.shortcuts import render

def imprimir_qr(request, id_reporte, formato):
    reporte = Reportes.objects.get(id_reporte=id_reporte)
    data = f"Nombre de máquina: {reporte.nombre_maquina}\nDescripción: {reporte.descripcion}\nNúmero de parte: {reporte.numero_parte}\nPiezas: {reporte.piezas}\nCosto: {reporte.costo}\nHoras: {reporte.horas}\nFecha de reemplazo: {reporte.fecha_reemplazo}\nFecha de reporte: {reporte.fecha_reporte}"
    qr_img = qrcode.make(data)

    # Generar archivo PNG
    if formato == 'png':
        qr_bytes = BytesIO()
        qr_img.save(qr_bytes, format='PNG')
        response = HttpResponse(content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename=qr_{reporte.id_reporte}.png'
        response.write(qr_bytes.getvalue())

        return response

    return redirect('reportes')


class reporteList(APIView):
    def get(self, request):
        Reportes = Reportes.objects.all()
        serializer = ReporteSerializer(Reportes, many=True)
        return Response(serializer.data)

class reporteDetail(APIView):
    def get(self, request, id_reporte):
        reporte = Reportes.objects.get(id_reporte=id_reporte)
        serializer = ReporteSerializer(reporte)
        return Response(serializer.data)
