from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
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
from .models import DatosAdministrador, DatosTecnico, Administrador, Tecnico
from .forms import DatosAdministradorForm, DatosTecnicoForm,CustomUserCreationForm, AdministradorForm, TecnicoForm



def inicio(request):


    return render(request, 'inicio.html')
    

def registrar(request):
    if request.method == 'POST':
        if 'registrar_administrador' in request.POST:
            user_form = AdministradorForm(request.POST)
            if user_form.is_valid():
                # Lógica para registrar un administrador
                email = user_form.cleaned_data['email']
                password1 = user_form.cleaned_data['password1']
                password2 = user_form.cleaned_data['password2']
                if Administrador.objects.filter(username=user_form.cleaned_data['username']).exists():
                    user_form.add_error('username', 'Este usuario ya existe, inténtelo de nuevo.')
                elif Administrador.objects.filter(email=email).exists():
                    user_form.add_error('email', 'Este correo ya está registrado, inténtelo de nuevo.')
                elif password1 != password2:
                    user_form.add_error('password2', 'Las contraseñas no coinciden.')
                else:
                    user = user_form.save()
                    user.is_active = True
                    administrador = Administrador(email=user.email)
                    administrador.save()
                    print(request.POST)
                    login(request, user)
                    return redirect('reportes')
        elif 'registrar_tecnico' in request.POST:
            user_form = TecnicoForm(request.POST)
            if user_form.is_valid():
                # Lógica para registrar un técnico
                email = user_form.cleaned_data['email']
                password1 = user_form.cleaned_data['password1']
                password2 = user_form.cleaned_data['password2']
                if Tecnico.objects.filter(username=user_form.cleaned_data['username']).exists():
                    user_form.add_error('username', 'Este usuario ya existe, inténtelo de nuevo.')
                elif Tecnico.objects.filter(email=email).exists():
                    user_form.add_error('email', 'Este correo ya está registrado, inténtelo de nuevo.')
                elif password1 != password2:
                    user_form.add_error('password2', 'Las contraseñas no coinciden.')
                else:
                    user = user_form.save(commit = False)
                    user.is_active = True
                    tecnico = Tecnico(email=user.email)
                    tecnico.save()
                    print(request.POST)
                    login(request, user)
                    return redirect('inicio')
    else:
        user_form = CustomUserCreationForm()

    return render(request, 'registrar.html', {'user_form': user_form})





#def registrar_administrador(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        datos_form = DatosAdministradorForm(request.POST)
        if user_form.is_valid() and datos_form.is_valid():
            email = user_form.cleaned_data['email']
            password1 = user_form.cleaned_data['password1']
            password2 = user_form.cleaned_data['password2']
            
            if User.objects.filter(username=user_form.cleaned_data['username']).exists():
                user_form.add_error('username', 'Este usuario ya existe intente otra vez.')
            elif User.objects.filter(email=email).exists():
                user_form.add_error('email', 'Este correo ya esta registrado intente otra vez.')
            elif password1 != password2:
                user_form.add_error('password2', 'Las contraseñas no coinciden.')
            else:
                user = user_form.save()
                administrador = Administrador(user=user, email=user.email)
                administrador.save()
                print(request.POST)
                login(request, user)  # Inicia sesión automáticamente después del registro
                return redirect('reportes')
    else:
        user_form = CustomUserCreationForm()
        datos_form = DatosTecnicoForm()

    return render(request, 'registrar_administrador.html', {'user_form': user_form, 'datos_form': datos_form})

#def registrar_tecnico(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)

        if user_form.is_valid():
            email = user_form.cleaned_data['email']
            password1 = user_form.cleaned_data['password1']
            password2 = user_form.cleaned_data['password2']
            
            if User.objects.filter(username=user_form.cleaned_data['username']).exists():
                user_form.add_error('username', 'Este usuario ya existe intente otra vez.')
            elif User.objects.filter(email=email).exists():
                user_form.add_error('email', 'Este correo ya está registrado intente otra vez.')
            elif password1 != password2:
                user_form.add_error('password2', 'Las contraseñas no coinciden.')
            else:
                user = user_form.save()
                tecnico = Tecnico(user=user, email=user.email)
                tecnico.save()
                print(request.POST)
                login(request, user)  # Inicia sesión automáticamente después del registro
                return redirect('inicio')
    else:
        user_form = CustomUserCreationForm()

    return render(request, 'registrar_tecnico.html', {'user_form': user_form})


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

def csesion(request):
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

