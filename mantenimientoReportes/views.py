from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .filters import InventarioFilter
from .forms import  MaquinaForm, InventarioForm, PartesForm, ReporteForm, ReporteUpdateForm
from .models import Historial, Maquina, Inventario, Partes, Reportes
from django.contrib import messages
import qrcode
import os
from io import BytesIO
from django.core.files import File
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReporteSerializer
from uuid import uuid4
import shutil
import uuid
from django.db.models import Q
from django.http import FileResponse 
import io
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .models import Reportes

@login_required
def panel(request):
    maquinas = Maquina.objects.all()
    context = {'maquinas': maquinas}
    return render(request,'panel.html', context)

@login_required
def nueva_maquina(request):
    if request.method == 'POST':
        form = MaquinaForm(request.POST, request.FILES)
        if form.is_valid():
            maquina = form.save(commit=False)
            maquina.user = request.user  # Asigna el usuario actual
            maquina.save()
            return redirect('panel')
    else:
        form = MaquinaForm()

    context = {'form': form}
    return render(request, 'nueva_maquina.html', context)

@login_required
def modificar_maquina(request, maquina_id):
    maquina = get_object_or_404(Maquina, pk=maquina_id)

    if request.method == "POST":
        form = MaquinaForm(request.POST, instance=maquina)
        if form.is_valid():
            form.save()
            return redirect('panel')  # Redirige a la página de maquinas después de guardar
    else:
        form = MaquinaForm(instance=maquina)

    return render(request, 'modificar_maquina.html', {'form': form, 'maquina': maquina})

@login_required
def eliminar_maquina(request, maquina_id):
    try:
        maquina = Maquina.objects.get(id=maquina_id)
    except Maquina.DoesNotExist:
        raise Http404("La máquina que intentas eliminar no existe.")
    
    if request.method == 'POST':
        if maquina.foto_maquina:
            if os.path.isfile(maquina.foto_maquina.path):
                os.remove(maquina.foto_maquina.path)
        maquina.delete()
        messages.success(request, 'La máquina ha sido eliminada exitosamente.')
        return redirect('panel')
    
    return render(request, 'eliminar_maquina.html', {'maquina': maquina})



@login_required
def inventario(request):
    inventario = Inventario.objects.filter(user=request.user)
    queryset = Inventario.objects.filter(user=request.user)
    filter = InventarioFilter(request.GET, queryset=queryset)

    elementos_por_pagina = 10
    paginator = Paginator(filter.qs, elementos_por_pagina)

    page = request.GET.get('page')

    try:
        inventario_paginado = paginator.page(page)
    except PageNotAnInteger:
        inventario_paginado = paginator.page(1)
    except EmptyPage:
        inventario_paginado = paginator.page(paginator.num_pages)

    

    return render(request, 'inventario.html', {'inventario': inventario_paginado, 'filter': filter})






@login_required
def nuevo_inventario(request):
    if request.method == 'POST':
        form = InventarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('inventario')
    else:
        form = InventarioForm()

    return render(request, 'nuevo_inventario.html', {'form': form})



@login_required
def eliminar_inventario(request, inventario_id):
    if request.method == 'POST':
        inventario = get_object_or_404(Inventario, id=inventario_id)

        # Guarda la ruta del archivo de imagen
        imagen_path = inventario.foto_partes.path

        # Elimina la entrada del inventario
        inventario.delete()

        # Verifica si la foto existe y la elimina del sistema de archivos
        if os.path.exists(imagen_path):
            os.remove(imagen_path)

        return redirect('inventario')

    return redirect('inventario')

@login_required
def modificar_inventario(request, inventario_id):
    inventario = get_object_or_404(Inventario, id=inventario_id)

    if request.method == 'POST':
        form = InventarioForm(request.POST, request.FILES, instance=inventario)
        if form.is_valid():
            form.save()
            return redirect('inventario')
    else:
        form = InventarioForm(instance=inventario)

    return render(request, 'modificar_inventario.html', {'form': form, 'inventario': inventario})

@login_required
def partes(request, maquina_id):
    maquina = get_object_or_404(Maquina, pk=maquina_id)
    # Obtiene todas las partes relacionadas con la máquina y el usuario actual
    partes = Partes.objects.filter(user=request.user, maquinas__id=maquina_id)


    # Paginación
    page = request.GET.get('page', 1)
    paginator = Paginator(partes, 10)  # Muestra 10 partes por página
    try:
        partes = paginator.page(page)
    except PageNotAnInteger:
        partes = paginator.page(1)
    except EmptyPage:
        partes = paginator.page(paginator.num_pages)

    # Renderiza la página 'partes' con la lista de partes
    return render(request, 'partes.html', {'partes': partes, 'maquina': maquina, 'filter': filter})


@login_required
def nuevo_partes(request, maquina_id):
    maquina = get_object_or_404(Maquina, pk=maquina_id)

    if request.method == 'POST':
        form = PartesForm(request.POST, request.FILES)
        if form.is_valid():
            # Asigna el usuario actual y la máquina al campo 'user' y 'maquinas' del formulario
            form.instance.user = request.user
            form.instance.maquinas = maquina

            # Guarda la nueva parte
            nueva_parte = form.save()

            # Verifica si la parte existe en el Inventario
            inventario_existente = Inventario.objects.filter(
                nombre_partes=nueva_parte.nombre_partes,
                numero_partes=nueva_parte.numero_partes
            ).first()

            if not inventario_existente:
                # Crea el objeto Inventario si no existe
                Inventario.objects.create(
                    user=request.user,
                    nombre_partes=nueva_parte.nombre_partes,
                    numero_partes=nueva_parte.numero_partes,
                    costo_aproximado=nueva_parte.costo_aproximado,
                    horas_uso=nueva_parte.horas_uso,
                    foto_partes=nueva_parte.foto_partes
                )

            return redirect('partes', maquina_id=maquina_id)
    else:
        form = PartesForm()

    return render(request, 'nuevo_partes.html', {'form': form, 'maquina': maquina})


@login_required
def eliminar_partes(request, partes_id):
    if request.method == 'POST':
        parte = get_object_or_404(Partes, id=partes_id)
        maquina_id = parte.maquinas.id if parte.maquinas else None
        # Guarda la ruta del archivo de imagen
        imagen_path = parte.foto_partes.path

        # Elimina la parte, pero no la pieza del inventario
        parte.delete()

        # Verifica si la foto existe y la elimina del sistema de archivos
        if os.path.exists(imagen_path):
            os.remove(imagen_path)

        if maquina_id:
            return redirect('partes', maquina_id=maquina_id)  # Reemplaza 'partes' con el nombre de tu vista de partes principal

    # Si la solicitud no es POST, puedes mostrar un mensaje de error o redirigir a alguna otra vista.
    return redirect('partes')

@login_required
def modificar_partes(request, partes_id):
    parte = get_object_or_404(Partes, id=partes_id)

    if request.method == 'POST':
        # Procesa el formulario de modificación y guarda los cambios en la parte
        form = PartesForm(request.POST, request.FILES, instance=parte)
        if form.is_valid():
            form.save()
            return redirect('partes')
    else:
        form = PartesForm(instance=parte)

    # Renderiza la página 'modificar_partes' con el formulario para modificar la parte
    return render(request, 'modificar_partes.html', {'form': form, 'parte': parte})

@login_required
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
    data = f"Nombre de máquina: {reporte.nombre_maquina}\nDescripción: {reporte.descripcion}\nNúmero de parte: {reporte.numero_parte}\nPiezas: {reporte.piezas}\nCosto: {reporte.costo}\nHoras: {reporte.horas}\nFecha de reemplazo: {reporte.fecha_reemplazo}\nFecha de reporte: {reporte.fecha_reporte}"
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