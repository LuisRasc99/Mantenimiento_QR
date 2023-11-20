from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .filters import InventarioFilter
from .models import Maquina, Inventario
from django.contrib import messages
import qrcode
import os
from io import BytesIO
from django.core.files import File
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from uuid import uuid4
import shutil
import uuid
from django.db.models import Q
from django.http import FileResponse 
import io
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def maquina(request):
    maquinas = Maquina.objects.all()
    context = {'maquinas': maquinas}
    return render(request, 'panel.html', context)
