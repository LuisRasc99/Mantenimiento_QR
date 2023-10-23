from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReporteForm, ReporteUpdateForm
from .models import Historial, Reportes
from django.contrib import messages
import qrcode
import os
from io import BytesIO
from django.core.files import File
from django.http import HttpResponse
import shutil
import uuid
from django.db.models import Q
from django.utils import timezone



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
            # Guardar los cambios en el reporte
            reporte = form.save()
            
            # Crear un objeto en la tabla de historial y copiar los valores originales
            historial = Historial.objects.create(
                reporte=reporte,
                nombre_maquina_anterior=reporte.nombre_maquina,
                descripcion_anterior=reporte.descripcion,
                numero_parte_anterior=reporte.numero_parte,
                piezas_anterior=reporte.piezas,
                costo_anterior=reporte.costo,
                horas_anterior=reporte.horas,
                fecha_reemplazo_anterior=reporte.fecha_reemplazo,
                usuario_modificacion=request.user,  # Asignar el usuario actual
                tipo_modificacion="Modificación",
                fecha_modificacion=timezone.now()
                
            )
            
            # Generar el QR en el historial
            historial.generar_qr_anterior()
            
            # Guardar los cambios en el reporte
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



def historial_reportes(request, reporte_id):
    reporte = get_object_or_404(Reportes, id_reporte=reporte_id)
    historiales = Historial.objects.filter(reporte=reporte).order_by('-fecha_modificacion')

    context = {
        'reporte': reporte,
        'historiales': historiales,
    }

    return render(request, 'historial_reportes.html', context)

@login_required
def eliminar_historial(request, id_historial):
    historial = get_object_or_404(Historial, pk=id_historial)

    if request.method == 'POST':
        # Eliminar el historial primero para evitar que se eliminen los archivos antes de copiarlos
        reporte_id = historial.reporte.id_reporte  # Guarda el ID del reporte antes de eliminar el historial
        historial.delete()
        
        # Luego, redirige al historial del reporte después de eliminar el historial
        messages.success(request, 'El historial ha sido eliminado exitosamente.')
        return redirect('historial_reportes', reporte_id=reporte_id)

    context = {'historial': historial}
    return redirect('historial_reportes', reporte_id=historial.reporte.id_reporte)


@login_required
def imprimir_qr_anterior(request, id_historial, formato):
    historial = Historial.objects.get(pk=id_historial)
    data = f"Nombre de máquina anterior: {historial.nombre_maquina_anterior}\nDescripción anterior: {historial.descripcion_anterior}\nNúmero de parte anterior: {historial.numero_parte_anterior}\nPiezas anteriores: {historial.piezas_anterior}\nCosto anterior: {historial.costo_anterior}\nHoras anteriores: {historial.horas_anterior}\nFecha de reemplazo anterior: {historial.fecha_reemplazo_anterior}\nFecha de modificación: {historial.fecha_modificacion}"
    
    qr_img = qrcode.make(data)

    # Generar archivo PNG
    if formato == 'png':
        qr_bytes = BytesIO()
        qr_img.save(qr_bytes, format='PNG')
        response = HttpResponse(content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename=qr_anterior_{historial.id}.png'
        response.write(qr_bytes.getvalue())

        return response

    return redirect('historial_reporte', reporte_id=historial.reporte.id_reporte)