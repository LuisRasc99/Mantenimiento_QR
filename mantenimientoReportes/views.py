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





