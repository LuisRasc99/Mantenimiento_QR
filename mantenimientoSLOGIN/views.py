from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomAuthenticationForm, DatosAdministradorForm, TecnicosForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.db.models import Q
from mantenimientoReportes.models import Reportes
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mantenimientoReportes.serializers import ReporteSerializer
from mantenimientoReportes.models import Reportes
from .models import DatosAdministrador, DatosTecnicos



def inicio(request):


    return render(request, 'inicio.html')
    
    

def registrar(request):


    return render(request, 'registrar.html', {

    })


#def registrar_tecnicos(request):
    if request.method == 'POST':
        form = AdministradorCreationForm(request.POST)
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
        form = AdministradorCreationForm()
    
    return render(request, 'registrar_tecnicos.html', {'form': form})

#def registrar_usuario(request):
    if request.method == 'GET':
        return render(request, 'registrar_usuario.html', {'form': AdministradorCreationForm()})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            username = request.POST['username']
            email = request.POST['email']
            
            # Verificar si el usuario ya existe
            if User.objects.filter(username=username).exists():
                return render(request, 'registrar_usuario.html', {
                    'form': AdministradorCreationForm(),
                    'error': 'El nombre de usuario ya existe'
                })
            
            # Verificar si el correo electrónico ya existe
            if User.objects.filter(email=email).exists():
                return render(request, 'registrar_usuario.html', {
                    'form': AdministradorCreationForm(),
                    'error': 'El correo electrónico ya está en uso'
                })
            
            try:
                user = User.objects.create_user(username=username, email=email, password=request.POST['password1'])
                user.profile.rol = 'usuario'  # Asignar el rol "usuario" al usuario
                user.save()
                login(request, user)
                return redirect('DatosAdministrador')
            except:
                return render(request, 'registrar_usuario.html', {
                    'form': AdministradorCreationForm(),
                    'error': 'Error al crear el usuario'
                })
        else:
            return render(request, 'registrar_usuario.html', {
                    'form': AdministradorCreationForm(),
                    'error': 'Las contraseñas no coinciden'
                })#




#def isesion(request):
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


#def csesion(request):
    logout(request)
    return redirect('inicio')

#def DatosAdministrador(request):
    if request.method == 'POST':
        datosform = DatosAdministradorForm(request.POST)
        if datosform.is_valid():
            datos_usuario = datosform.save(commit=False)
            datos_usuario.user = request.user
            datos_usuario.save()
            return redirect('reportes')  #Reemplaza 'otra_pagina' con la URL a la que deseas redirigir después de guardar los datos
    else:
        datosform = DatosAdministradorForm()
    return render(request, 'DatosAdministrador.html', {'datosform': datosform})

#def modificar_datos(request):
    user = request.user
    try:
        datos_usuario = user.DatosAdministrador
    except DatosAdministrador.DoesNotExist:
        datos_usuario = None

    if request.method == 'POST':
        form = DatosAdministradorForm(request.POST, instance=datos_usuario)
        if form.is_valid():
            datos_usuario = form.save(commit=False)
            datos_usuario.user = request.user
            datos_usuario.save()
            return redirect('reportes')  # Reemplaza 'reportes' con la URL a la que deseas redirigir después de guardar los datos
    else:
        form = DatosAdministradorForm(instance=datos_usuario)

    return render(request, 'modificar_datos.html', {'form': form})

    
#def lista_tecnicos(request):


    return render(request, 'lista_tecnicos.html')

