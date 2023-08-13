from django.shortcuts import render

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
from .models import Reportes


@login_required
def nuevo_reporte(request):
    if request.method == 'POST':
        nombre_maquina = request.POST.getlist('nombre_maquina[]')
        descripcion = request.POST.getlist('descripcion[]')
        numero_parte = request.POST.getlist('numero_parte[]')
        piezas = request.POST.getlist('piezas[]')
        costo = request.POST.getlist('costo[]')
        horas = request.POST.getlist('horas[]')
        fecha_reemplazo = request.POST.getlist('fecha_reemplazo[]')

        for i in range(len(nombre_maquina)):
            form_data = {
                'nombre_maquina': nombre_maquina[i],
                'descripcion': descripcion[i],
                'numero_parte': numero_parte[i],
                'piezas': piezas[i],
                'costo': costo[i],
                'horas': horas[i],
                'fecha_reemplazo': fecha_reemplazo[i]
            }
            form = ReporteForm(form_data, request.FILES)
            if form.is_valid():
                reporte = form.save(commit=False)
                reporte.user = request.user
                reporte.save()
                reporte.generar_qr()

        return redirect('reportes')
    return render(request, 'nuevo_reporte.html')

@login_required
def reportes(request):
    user = request.user
    reportes = Reportes.objects.filter(user=user)
    return render(request, 'reportes.html', {'reportes': reportes})

@login_required
def modificar_reporte(request, id_reporte):
    reporte = Reportes.objects.get(id_reporte=id_reporte)
    if request.method == 'POST':
        form = ReporteUpdateForm(request.POST, request.FILES, instance=reporte)
        if form.is_valid():
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
        if reporte.qr:
            if os.path.isfile(reporte.qr.path):
                os.remove(reporte.qr.path)
        reporte.delete()
        messages.success(request, 'El reporte ha sido eliminado exitosamente.')
        return redirect('reportes')
    return render(request, 'eliminar_reporte.html', {'reporte': reporte})

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
