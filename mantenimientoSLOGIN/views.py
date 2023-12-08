from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import DatosUsuarioForm, UsuarioForm
from .models import Usuario
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.user.is_authenticated:
            return response

        return redirect('iniciar_sesion')

def IniciarSesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirige según el tipo de usuario
            if user.tipo_usuario == 'administrador':
                return redirect('mantenimiento')
            elif user.tipo_usuario == 'tecnico':
                return redirect('panel_tecnico')
            elif user.is_superuser:
                messages.success(request, f'Bienvenido, {user.username}! Has iniciado sesión como Superusuario.')
                return redirect('admin:index')  # Redirige al panel de administración
        else:
            # Mensajes para diferentes escenarios de inicio de sesión fallido
            if user is None:
                messages.error(request, 'Credenciales incorrectas. Por favor, verifica tu usuario y contraseña.')
            elif not user.is_active:
                messages.error(request, 'Tu cuenta está desactivada. Comunícate con el administrador.')
            elif user is not None and not user.is_authenticated:
                messages.error(request, 'Error de autenticación. Comunícate con el soporte técnico.')

    return render(request, 'iniciar_sesion.html')

@login_required
def CerrarSesion(request):
    logout(request)
    return redirect('iniciar_sesion')

def Registrar(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            return redirect('iniciar_sesion')
    else:
        form = UsuarioForm()

    return render(request, 'registrar.html', {'form': form})

@login_required
def DatosUsuario(request, username):
    usuario_autenticado = request.user

    # Verifica si el usuario autenticado tiene permisos
    if not usuario_autenticado.has_perm('puede_agregar_datos_usuario'):
        messages.error(request, 'No tienes permisos para modificar estos datos.')
        return redirect('iniciar_sesion')  # Modifica esto según tu lógica

    usuario = get_object_or_404(Usuario, username=username)

    if not usuario.datos_usuario:
        if request.method == 'POST':
            form = DatosUsuarioForm(request.POST)
            if form.is_valid():
                datos_usuario = form.save(commit=False)
                datos_usuario.usuario = usuario
                datos_usuario.save()
                messages.success(request, 'Datos del usuario completados exitosamente.')

                # Redirige según el tipo de usuario
                if usuario.tipo_usuario == 'administrador':
                    return redirect('panel')
                elif usuario.tipo_usuario == 'tecnico':
                    return redirect('panel_tecnico')
        else:
            form = DatosUsuarioForm()

        return render(request, 'datos_usuario.html', {'form': form, 'usuario': usuario})


@login_required
def ModificarDatosUsuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        form = DatosUsuarioForm(request.POST, instance=usuario.datos_usuario)
        if form.is_valid():
            datos_usuario = form.save(commit=False)
            datos_usuario.usuario = usuario  # Asociar los datos al usuario correcto
            datos_usuario.save()
            return redirect('panel', usuario_id=usuario.id)
    else:
        form = DatosUsuarioForm(instance=usuario.datos_usuario)

    return render(request, 'modificar_datos.html', {'form': form, 'usuario': usuario})

@login_required
def Tecnicos(request):
    # Lógica para mostrar la lista de técnicos
    tecnicos = Usuario.objects.filter(tipo_usuario='tecnico')
    return render(request, 'lista_tecnicos.html', {'tecnicos': tecnicos})

@login_required
def RegistrarTecnicos(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            # Asegúrate de establecer el tipo de usuario como 'tecnico'
            form.instance.tipo_usuario = 'tecnico'
            user = form.save()
            messages.success(request, 'Técnico registrado exitosamente.')
            return redirect('tecnicos')
    else:
        form = UsuarioForm()

    return render(request, 'mantenimientoSLOGIN/registrar_tecnico.html', {'form': form})

