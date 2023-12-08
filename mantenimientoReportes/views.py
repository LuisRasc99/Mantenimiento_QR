from datetime import datetime, timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from django.contrib.auth.decorators import user_passes_test,login_required
from django.http import Http404, HttpResponse, HttpResponseBadRequest, JsonResponse
from appmantenimiento import settings
from .forms import InventarioEntradaForm, InventarioSalidaForm,MaquinaForm, CatalogoPartesForm
from mantenimientoSLOGIN.models import Usuario  # Asegúrate de importar tu modelo de usuario
from .models import Maquina, CatalogoPartes, MovimientoInventario
from django.shortcuts import get_object_or_404, redirect, render
from django.core.files.storage import default_storage
from django.contrib import messages
from django.db.models import Sum
from django.db.models import F
from django.db.models import Max
from django.db import transaction

# Decorador para permitir solo a los administradores
@user_passes_test(lambda u: u.is_authenticated and u.tipo_usuario == 'administrador', login_url='/iniciar_sesion/')
def panel(request):
    maquinas = Maquina.objects.filter(user=request.user)
    nombre_usuario = request.user.username  # Cambia esto según tu modelo de Usuario
    
    if request.method == 'POST':
        form = MaquinaForm(request.POST, request.FILES)
        if form.is_valid():
            maquina = form.save(commit=False)
            maquina.user = request.user  # Asigna el usuario actual
            maquina.save()
            return redirect('panel')
    else:
        form = MaquinaForm()
    
    
    context = {'form': MaquinaForm(),'maquinas': maquinas, 'nombre_usuario': nombre_usuario}
    return render(request, 'panel.html', context)

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
        print(request.POST)
        form = MaquinaForm(request.POST, request.FILES, instance=maquina)
        if form.is_valid():
            form.save()
            maquina.refresh_from_db()  # Actualiza la instancia desde la base de datos
            return redirect('panel')

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
    
    maquinas = Maquina.objects.filter(user=request.user)  # Agrega esto para obtener la lista actualizada de máquinas
    context = {'maquinas': maquinas}
    return render(request, 'panel.html', context)

@login_required
def partes(request):
    partes = CatalogoPartes.objects.filter(user=request.user)
    nombre_usuario = request.user.username

    if request.method == 'POST':
        form = CatalogoPartesForm(request.POST, request.FILES)
        if form.is_valid():
            parte = form.save(commit=False)
            parte.user = request.user
            parte.save()
            return redirect('partes')
    else:
        form = CatalogoPartesForm()

    context = {'form': form, 'partes': partes, 'nombre_usuario': nombre_usuario}
    return render(request, 'partes.html', context)



@login_required
def modificar_partes(request, parte_id):
    parte = get_object_or_404(CatalogoPartes, pk=parte_id)

    if request.method == "POST":
        form = CatalogoPartesForm(request.POST, request.FILES, instance=parte)
        if form.is_valid():
            form.save()
            parte.refresh_from_db()
            return redirect('partes')
    else:
        form = CatalogoPartesForm(instance=parte)

    return render(request, 'modificar_partes.html', {'form': form, 'parte': parte})

@login_required
def eliminar_partes(request, parte_id):
    try:
        parte = CatalogoPartes.objects.get(id=parte_id)
    except CatalogoPartes.DoesNotExist:
        raise Http404("La parte que intentas eliminar no existe.")

    if request.method == 'POST':
        if parte.foto_partes:
            if os.path.isfile(parte.foto_partes.path):
                os.remove(parte.foto_partes.path)
        parte.delete()
        messages.success(request, 'La parte ha sido eliminada exitosamente.')
        return redirect('partes')

    partes = CatalogoPartes.objects.filter(user=request.user)
    context = {'partes': partes}
    return render(request, 'partes.html', context)


@login_required
def inventario_entrada(request):
    inventario = MovimientoInventario.objects.filter(user=request.user, movimiento=True)
    partes = CatalogoPartes.objects.all()

    if request.method == 'POST':
        form = InventarioEntradaForm(request.POST)
        if form.is_valid():
            inventario_item = form.save(commit=False)
            inventario_item.user = request.user
            inventario_item.movimiento = True  # Indicar que es un movimiento de entrada
            inventario_item.entrada = datetime.now(timezone.utc)
            inventario_item.save()
            # Recuperar el objeto después de guardarlo
            inventario_item = get_object_or_404(MovimientoInventario, id=inventario_item.id)

            # Obtener el objeto relacionado a través de partes
            partes_obj = inventario_item.partes

            # Obtener el último movimiento relacionado con la misma parte
            ultimo_movimiento = MovimientoInventario.objects.filter(user=request.user, partes=partes_obj, movimiento=True).exclude(id=inventario_item.id).last()

            # Obtener el total_piezas del último movimiento o establecerlo en 0 si no hay movimientos previos
            total_piezas_anterior = ultimo_movimiento.total_piezas if ultimo_movimiento else 0

            # Actualizar total_piezas
            inventario_item.total_piezas = total_piezas_anterior + inventario_item.piezas_entrada
            inventario_item.save()

            print(f"partes: {inventario_item.partes}, piezas_entrada: {inventario_item.piezas_entrada}, total_piezas después del guardado: {inventario_item.total_piezas}")

            return redirect('inventario_entrada')
    else:
        form = InventarioEntradaForm()

        # Agregar paginación
    paginator = Paginator(inventario, 10)  # Muestra 10 entradas por página
    page = request.GET.get('page')

    try:
        inventario_pagina = paginator.page(page)
    except PageNotAnInteger:
        inventario_pagina = paginator.page(1)
    except EmptyPage:
        inventario_pagina = paginator.page(paginator.num_pages)

    context = {'inventario': inventario, 'form': form, 'partes': partes, 'inventario_pagina': inventario_pagina}
    return render(request, 'inventario_entrada.html', context)

@login_required
def editar_inventario_entrada(request, inventario_id):
    inventario = get_object_or_404(MovimientoInventario, pk=inventario_id, user=request.user, movimiento=True)

    if request.method == "POST":
        form = InventarioEntradaForm(request.POST, instance=inventario)
        if form.is_valid():
            inventario = form.save(commit=False)
            inventario.movimiento = True  # Asegurarse de que se mantiene como un movimiento de entrada
            inventario.save()
            return redirect('inventario_entrada')

    else:
        form = InventarioEntradaForm(instance=inventario)

    return render(request, 'editar_inventario.html', {'form': form, 'inventario_item': inventario})

@login_required
def eliminar_inventario_entrada(request, inventario_id):
    inventario = get_object_or_404(MovimientoInventario, id=inventario_id, user=request.user, movimiento=True)
    
    if request.method == 'POST':
        inventario.delete()
        return redirect('inventario_entrada')

    return render(request, 'eliminar_inventario.html', {'inventario': inventario})

@login_required
def mantenimiento(request):
    mantenimiento_items = MovimientoInventario.objects.filter(user=request.user, movimiento=False)
    partes = CatalogoPartes.objects.all()
    maquinas = Maquina.objects.all()

    if request.method == 'POST':
        form = InventarioSalidaForm(request.POST)
        if form.is_valid():
            mantenimiento_item = form.save(commit=False)
            mantenimiento_item.user = request.user
            mantenimiento_item.movimiento = False  # Indicar que es un movimiento de salida (mantenimiento)
            mantenimiento_item.fecha_salida = datetime.now(timezone.utc)# Actualizar la fecha de entrada
            mantenimiento_item.save()
            
            inventario_item = get_object_or_404(MovimientoInventario, id=inventario_item.id)

            # Obtener el objeto relacionado a través de partes
            partes_obj = inventario_item.partes

            # Obtener el último movimiento relacionado con la misma parte
            ultimo_movimiento = MovimientoInventario.objects.filter(user=request.user, partes=partes_obj, movimiento=True).exclude(id=inventario_item.id).last()

            # Obtener el total_piezas del último movimiento o establecerlo en 0 si no hay movimientos previos
            total_piezas_anterior = ultimo_movimiento.total_piezas if ultimo_movimiento else 0

            # Actualizar total_piezas
            inventario_item.total_piezas = total_piezas_anterior - inventario_item.piezas_salida
            inventario_item.save()

            return redirect('mantenimiento')
    else:
        form = InventarioSalidaForm()

    # Agregar paginación
    paginator = Paginator(mantenimiento_items, 10)  # Muestra 10 entradas por página
    page = request.GET.get('page')

    try:
        mantenimiento_pagina = paginator.page(page)
    except PageNotAnInteger:
        mantenimiento_pagina = paginator.page(1)
    except EmptyPage:
        mantenimiento_pagina = paginator.page(paginator.num_pages)


    context = {'mantenimiento_items': mantenimiento_items, 'form': form, 'partes': partes, 'maquinas': maquinas, 'mantenimiento_pagina': mantenimiento_pagina}
    return render(request, 'mantenimiento.html', context)

@login_required
def editar_mantenimiento(request, mantenimiento_id):
    mantenimiento_item = get_object_or_404(MovimientoInventario, pk=mantenimiento_id, user=request.user, movimiento=False)

    # Obtener el valor actual de piezas_entrada
    piezas_entrada_anterior = mantenimiento_item.piezas_entrada

    if request.method == "POST":
        form = InventarioSalidaForm(request.POST, instance=mantenimiento_item)
        if form.is_valid():
            mantenimiento_item = form.save(commit=False)
            mantenimiento_item.movimiento = False  # Asegurarse de que se mantiene como un movimiento de salida (mantenimiento)
            mantenimiento_item.save()

            # Obtener el nuevo valor de piezas_entrada
            piezas_entrada_nueva = mantenimiento_item.piezas_entrada

            # Actualizar total_piezas según la diferencia
            diferencia_piezas = piezas_entrada_nueva - piezas_entrada_anterior
            mantenimiento_item.total_piezas = mantenimiento_item.total_piezas + diferencia_piezas
            mantenimiento_item.save()

            return redirect('mantenimiento')

    else:
        form = InventarioSalidaForm(instance=mantenimiento_item)

    return render(request, 'editar_inventario.html', {'form': form, 'mantenimiento_item': mantenimiento_item})

@login_required
def eliminar_mantenimiento(request, mantenimiento_id):
    mantenimiento_item = get_object_or_404(MovimientoInventario, id=mantenimiento_id, user=request.user, movimiento=False)

    # Obtener el valor de piezas_entrada antes de eliminar el registro
    piezas_entrada_eliminado = mantenimiento_item.piezas_entrada

    if request.method == 'POST':
        mantenimiento_item.delete()

        # Restar piezas_entrada al total_piezas
        mantenimiento_item.total_piezas = mantenimiento_item.total_piezas - piezas_entrada_eliminado
        mantenimiento_item.save()

        return redirect('mantenimiento')

    return render(request, 'eliminar_inventario.html', {'inventario': mantenimiento_item})

@login_required
def almacen(request):
    inventario = MovimientoInventario.objects.all()
    partes = CatalogoPartes.objects.all()

    # Agregar paginación
    paginator = Paginator(inventario, 10)  # Muestra 10 entradas por página
    page = request.GET.get('page')

    try:
        almacen_pagina = paginator.page(page)
    except PageNotAnInteger:
        almacen_pagina = paginator.page(1)
    except EmptyPage:
        almacen_pagina = paginator.page(paginator.num_pages)

    context = {'almacen_pagina': almacen_pagina, 'partes': partes}
    return render(request, 'almacen.html', context)