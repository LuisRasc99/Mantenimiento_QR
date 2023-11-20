from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import DatosUsuarioForm, UsuarioForm
from .models import Usuario


def IniciarSesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                if user.tipo_usuario == 'administrador':
                    return redirect('panel')
                elif user.tipo_usuario == 'tecnico':
                    return redirect('panel_tecnico')
        else:
            messages.error(request, 'Credenciales incorrectas. Por favor, inténtalo de nuevo.')

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
    # Verifica que el usuario autenticado tenga los permisos adecuados
    if not request.user.is_superuser and (request.user.tipo_usuario == 'tecnico' or (request.user.tipo_usuario == 'administrador' and request.user.username != username)):
        messages.error(request, 'No tienes permisos para modificar estos datos.')
        return redirect('isesion')

    # Obtiene el usuario a modificar
    usuario = get_object_or_404(Usuario, username=username)

    if request.method == 'POST':
        form = DatosUsuarioForm(request.POST, instance=usuario.datos_usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos del usuario actualizados exitosamente.')
            return redirect('isesion')  # Redirige a la página principal después de actualizar los datos
    else:
        form = DatosUsuarioForm(instance=usuario.datos_usuario)

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

