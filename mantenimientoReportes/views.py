import os
from django.contrib.auth.decorators import user_passes_test,login_required
from django.http import Http404, HttpResponse, HttpResponseBadRequest, JsonResponse
from appmantenimiento import settings
from .forms import InventarioForm, MantenimientoPartesForm, MaquinaForm, CatalogoPartesForm
from mantenimientoSLOGIN.models import Usuario  # Asegúrate de importar tu modelo de usuario
from .models import Inventario, InventarioStock, MantenimientoPartes, Maquina, CatalogoPartes
from django.shortcuts import get_object_or_404, redirect, render
from django.core.files.storage import default_storage
from django.contrib import messages
from django.db.models import Sum
from django.db.models import F

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
def mantenimiento_partes(request):
    mantenimientos = MantenimientoPartes.objects.all()

    if request.method == 'POST':
        form = MantenimientoPartesForm(request.POST)
        if form.is_valid():
            mantenimiento = form.save(commit=False)
            mantenimiento.user = request.user
            mantenimiento.save()

            maquina = get_object_or_404(Maquina, id=mantenimiento.maquina.id)
            
            # Verifica si el campo 'hrs' existe en el formulario antes de asignarlo
            if 'hrs' in form.cleaned_data:
                maquina.horas_maquina = mantenimiento.hrs
                maquina.save()

            return redirect('mantenimiento_partes')
    else:
        form = MantenimientoPartesForm()

    maquinas = Maquina.objects.all()
    partes = CatalogoPartes.objects.all()

    context = {'form': form, 'mantenimientos': mantenimientos, 'maquinas': maquinas, 'partes': partes}
    return render(request, 'mantenimiento_partes.html', context)

@login_required
def editar_mantenimiento(request, mantenimiento_id):
    mantenimiento = get_object_or_404(MantenimientoPartes, id=mantenimiento_id)

    if request.method == 'POST':
        form = MantenimientoPartesForm(request.POST, instance=mantenimiento)
        if form.is_valid():
            mantenimiento = form.save(commit=False)
            mantenimiento.user = request.user
            mantenimiento.save()

            maquina = get_object_or_404(Maquina, id=mantenimiento.maquina.id)
            maquina.horas_maquina += mantenimiento.hrs
            maquina.save()

            return redirect('mantenimiento_partes')
    else:
        form = MantenimientoPartesForm(instance=mantenimiento)

    maquinas = Maquina.objects.all()
    partes = CatalogoPartes.objects.all()
    context = {'form': form, 'maquinas': maquinas, 'partes': partes}
    return render(request, 'editar_mantenimiento.html', context)

@login_required
def eliminar_mantenimiento(request, mantenimiento_id):
    try:
        mantenimiento = MantenimientoPartes.objects.get(id=mantenimiento_id)
    except MantenimientoPartes.DoesNotExist:
        raise Http404("El mantenimiento que intentas eliminar no existe.")

    if request.method == 'POST':
        mantenimiento.delete()
        messages.success(request, 'El mantenimiento ha sido eliminada exitosamente.')
        return redirect('mantenimiento_partes')

    mantenimientos = MantenimientoPartes.objects.filter(user=request.user)
    context = {'mantenimientos': mantenimientos}
    return render(request, 'mantenimiento_partes.html', context)


@login_required
def inventario(request):
    inventarios = Inventario.objects.all()

    if request.method == 'POST':
        form = InventarioForm(request.POST)
        if form.is_valid():
            inventario_nuevo = form.save(commit=False)
            inventario_nuevo.user = request.user
            inventario_nuevo.save()

            # Obtén o crea un objeto InventarioStock asociado a este Inventario
            inventario_stock, created = InventarioStock.objects.get_or_create(
                partes=inventario_nuevo.partes,
                defaults={'inventario': inventario_nuevo}
            )

            # Obtén el objeto antes de realizar la operación de guardado
            inventario_stock.refresh_from_db()

            # Actualiza la cantidad_piezas y costo_total en InventarioStock
            inventario_stock.cantidad_piezas = F('cantidad_piezas') + inventario_nuevo.piezas_entrada
            inventario_stock.costo_total = F('costo_total') + inventario_nuevo.partes.costo_aproximado * inventario_nuevo.piezas_entrada
            inventario_stock.save()

            return redirect('inventario')
        else:
            print(form.errors)  # Imprime los errores del formulario en la consola
    else:
        form = InventarioForm()

    partes = CatalogoPartes.objects.all()
    mantenimientos = MantenimientoPartes.objects.all()

    context = {'form': form, 'inventarios': inventarios, 'partes': partes, 'mantenimientos': mantenimientos}
    return render(request, 'inventario.html', context)


    

@login_required
def editar_inventario(request, inventario_id):
    inventario = get_object_or_404(Inventario, id=inventario_id)

    if request.method == 'POST':
        form = InventarioForm(request.POST, instance=inventario)
        if form.is_valid():
            inventario = form.save(commit=False)
            inventario.user = request.user
            inventario.save()
            return redirect('inventario')
    else:
        form = InventarioForm(instance=inventario)

    partes = CatalogoPartes.objects.all()
    mantenimientos = MantenimientoPartes.objects.all()

    context = {'form': form, 'partes': partes, 'mantenimientos': mantenimientos}
    return render(request, 'editar_inventario.html', context)

@login_required
def eliminar_inventario(request, inventario_id):
    inventario = get_object_or_404(Inventario, id=inventario_id)

    if request.method == 'POST':
        # Guarda la información antes de eliminar el inventario

        partes = inventario.partes

        # Elimina el inventario
        inventario.delete()
        messages.success(request, 'El inventario ha sido eliminado exitosamente.')

        # Actualiza la cantidad_piezas en InventarioStock
        inventario_stock = InventarioStock.objects.filter(
            partes=partes
        ).first()

        if inventario_stock:
            total_piezas = Inventario.objects.filter(
                partes=partes
            ).aggregate(Sum('piezas_entrada'))['piezas_entrada__sum'] or 0

            inventario_stock.cantidad_piezas = total_piezas
            inventario_stock.costo_total = partes.costo_aproximado * total_piezas
            inventario_stock.save()

        return redirect('inventario')

    inventarios = Inventario.objects.filter(user=request.user)
    context = {'inventarios': inventarios}
    return render(request, 'inventario.html', context)

@login_required
def inventario_stock(request):
    inventarios_stock = InventarioStock.objects.all()
    inventarios = Inventario.objects.all()
    partes = CatalogoPartes.objects.all()
    
    context = {'inventarios_stock': inventarios_stock, 'inventarios': inventarios, 'partes': partes}
    return render(request, 'inventario_stock.html', context)


@login_required
def inventario_salida(request):
    inventarios = Inventario.objects.all()
    mantenimientos = MantenimientoPartes.objects.all()
    
    context = {'inventarios': inventarios, 'mantenimientos': mantenimientos}
    return render(request, 'inventario_salida.html', context)