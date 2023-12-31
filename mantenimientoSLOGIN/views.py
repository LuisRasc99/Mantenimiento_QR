from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm, DatosUsuarioForm, TecnicosForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.db.models import Q
from mantenimientoReportes.models import Reportes
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import DatosUsuarioSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mantenimientoReportes.serializers import ReporteSerializer
from mantenimientoReportes.models import Reportes
from .models import DatosTecnicos



def inicio(request):
    if request.method == 'POST':
        buscar = request.POST.get('buscar')
        if buscar:  # Verifica si el campo de búsqueda no está vacío
            reportes = Reportes.objects.filter(nombre_maquina__icontains=buscar)
        else:
            reportes = None
    else:
        reportes = None

    return render(request, 'inicio.html', {'reportes': reportes})
    
    
from .forms import CustomUserCreationForm, TecnicosForm

def registrar(request):
    form_usuario = CustomUserCreationForm()
    form_tecnicos = TecnicosForm()  # Agregar el formulario de técnicos

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            rol = form.cleaned_data['rol']

            # Verificar si el usuario ya existe
            if User.objects.filter(username=username).exists():
                return render(request, 'registrar.html', {
                    'form_usuario': form,
                    'form_tecnicos': form_tecnicos,  # Pasar el formulario de técnicos al contexto
                    'error': 'El nombre de usuario ya existe'
                })

            user = form.save()
            user.refresh_from_db()
            user.profile.rol = rol

            if rol == 'tecnico':
                email = form.cleaned_data['email']
                user.email = email
                user.save()

            login(request, user)

            if rol == 'administrador':
                return redirect('datosusuario')
            elif rol == 'tecnico':
                return redirect('datostecnico')

    return render(request, 'registrar.html', {
        'form_usuario': form_usuario,
        'form_tecnicos': form_tecnicos,  # Pasar el formulario de técnicos al contexto
    })


def registrar_tecnicos(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Verificar si el usuario ya existe
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                return render(request, 'registrar_tecnicos.html', {
                    'form': form,
                    'error': 'El nombre de usuario ya existe'
                })

            # Verificar si el correo electrónico ya existe
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                return render(request, 'registrar_tecnicos.html', {
                    'form': form,
                    'error': 'El correo electrónico ya está en uso'
                })

            # Verificar que las contraseñas coincidan
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 != password2:
                return render(request, 'registrar_tecnicos.html', {
                    'form': form,
                    'error': 'Las contraseñas no coinciden'
                })

            # Si todas las verificaciones pasan, guarda los datos del técnico
            user = form.save()
            user.profile.rol = 'tecnico'  # Asignar el rol "tecnico" al usuario
            user.save()
            # Realiza cualquier otra acción que necesites, como redireccionar a la lista de técnicos
            return redirect('lista_tecnicos')  # Cambia 'lista_tecnicos' al nombre de la vista que muestre la lista de técnicos
    else:
        form = UserCreationForm()
    
    return render(request, 'registrar_tecnicos.html', {'form': form})

def registrar_usuario(request):
    if request.method == 'GET':
        return render(request, 'registrar_usuario.html', {'form': UserCreationForm()})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            username = request.POST['username']
            email = request.POST['email']
            
            # Verificar si el usuario ya existe
            if User.objects.filter(username=username).exists():
                return render(request, 'registrar_usuario.html', {
                    'form': UserCreationForm(),
                    'error': 'El nombre de usuario ya existe'
                })
            
            # Verificar si el correo electrónico ya existe
            if User.objects.filter(email=email).exists():
                return render(request, 'registrar_usuario.html', {
                    'form': UserCreationForm(),
                    'error': 'El correo electrónico ya está en uso'
                })
            
            try:
                user = User.objects.create_user(username=username, email=email, password=request.POST['password1'])
                user.profile.rol = 'usuario'  # Asignar el rol "usuario" al usuario
                user.save()
                login(request, user)
                return redirect('DatosUsuario')
            except:
                return render(request, 'registrar_usuario.html', {
                    'form': UserCreationForm(),
                    'error': 'Error al crear el usuario'
                })
        else:
            return render(request, 'registrar_usuario.html', {
                    'form': UserCreationForm(),
                    'error': 'Las contraseñas no coinciden'
                })




def isesion(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Intentar autenticar con el nombre de usuario
            user = authenticate(request=request, username=username, password=password)

            # Si la autenticación con el nombre de usuario falla, intentar con el correo electrónico
            if user is None:
                UserModel = get_user_model()
                try:
                    user = UserModel.objects.get(email=username)
                    user = authenticate(request=request, username=user.username, password=password)
                except UserModel.DoesNotExist:
                    pass

            if user is not None:
                login(request, user)
                return redirect('reportes')  # Redirigir a la página de inicio después del inicio de sesión exitoso
        else:
            error_message = 'Error al iniciar sesión. Por favor, verifica tus credenciales.'
            return render(request, 'isesion.html', {'isesionform': form, 'error_message': error_message})
    else:
        form = CustomAuthenticationForm()
    return render(request, 'isesion.html', {'isesionform': form})


def csesion(request):
    logout(request)
    return redirect('inicio')

def DatosUsuario(request):
    if request.method == 'POST':
        datosform = DatosUsuarioForm(request.POST)
        if datosform.is_valid():
            datos_usuario = datosform.save(commit=False)
            datos_usuario.user = request.user
            datos_usuario.save()
            return redirect('reportes')  #Reemplaza 'otra_pagina' con la URL a la que deseas redirigir después de guardar los datos
    else:
        datosform = DatosUsuarioForm()
    return render(request, 'datosusuario.html', {'datosform': datosform})

def modificar_datos(request):
    user = request.user
    try:
        datos_usuario = user.datosusuario
    except DatosUsuario.DoesNotExist:
        datos_usuario = None

    if request.method == 'POST':
        form = DatosUsuarioForm(request.POST, instance=datos_usuario)
        if form.is_valid():
            datos_usuario = form.save(commit=False)
            datos_usuario.user = request.user
            datos_usuario.save()
            return redirect('reportes')  # Reemplaza 'reportes' con la URL a la que deseas redirigir después de guardar los datos
    else:
        form = DatosUsuarioForm(instance=datos_usuario)

    return render(request, 'modificar_datos.html', {'form': form})

@api_view(['GET'])
def api_inicio(request):
    if request.method == 'GET':
        reportes = Reportes.objects.all()
        serializer = ReporteSerializer(reportes, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def api_datos_usuario(request):
    if request.method == 'POST':
        serializer = DatosUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReporteList(APIView):
    def get(self, request):
        reportes = Reportes.objects.all()
        serializer = ReporteSerializer(reportes, many=True)
        return Response(serializer.data)

class ReporteDetail(APIView):
    def get(self, request, id_reporte):
        reporte = Reportes.objects.get(id_reporte=id_reporte)
        serializer = ReporteSerializer(reporte)
        return Response(serializer.data)
    
def lista_tecnicos(request):


    return render(request, 'lista_tecnicos.html')

