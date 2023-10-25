from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm, RegistroForm,  PerfilForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from mantenimientoReportes.models import Reportes
from rest_framework.decorators import api_view
from mantenimientoReportes.models import Reportes
from .models import Usuario, DatosAdministrador, DatosTecnico
from django.contrib.auth.decorators import login_required




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
    
    
def registrar(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            rol = form.cleaned_data['rol']

            # Comprobar si el usuario ya existe
            if Usuario.objects.filter(username=username).exists():
                form.add_error('username', 'El nombre de usuario ya existe')

            # Comprobar si el correo ya existe
            if Usuario.objects.filter(email=email).exists():
                form.add_error('email', 'El correo ya está en uso')

            # Comprobar si las contraseñas coinciden
            if password1 != password2:
                form.add_error('password1', 'Las contraseñas no coinciden')
                form.add_error('password2', 'Las contraseñas no coinciden')

            # Comprobar si se eligió un rol
            if not rol:
                form.add_error('rol', 'Debes seleccionar un rol')

            try:
                usuario = Usuario.objects.create_user(username=username, email=email, password=form.cleaned_data['password1'], rol=rol)
                usuario.save()
                login(request, usuario)
                
                # Redirigir según el rol
                if rol == 'administrador':
                    return redirect('PerfilUsuario')  # Reemplaza 'pagina_administrador' con la URL de la página de administrador.
                elif rol == 'tecnico':
                    return redirect('PerfilUsuario')  # Reemplaza 'pagina_tecnico' con la URL de la página de técnico.
            except:
                return render(request, 'registrar.html', {
                    'form': form,
                    'error': 'Error al crear el usuario'
                })

    else:
        form = RegistroForm()
    
    return render(request, 'registrar.html', {'form': form})


def PerfilUsuario(request):
    if request.method == 'POST':
        datosform = PerfilForm(request.POST)
        if datosform.is_valid():
            if request.user.is_authenticated:
                # Si el usuario está autenticado, guarda los datos del administrador
                datos_administrador = datosform.save(commit=False)
                datos_administrador.usuario = request.user
                datos_administrador.save()
                return redirect('reportes')  # Reemplaza 'reportes' con la URL a la que deseas redirigir después de guardar los datos
            else:
                # Si el usuario no está autenticado, puedes guardar los datos en una sesión temporal
                request.session['perfil_usuario_temp'] = datosform.cleaned_data
                return redirect('registrar')  # Redirigir al usuario a la página de inicio de sesión
    else:
        datosform = PerfilForm()
    return render(request, 'perfil_usuario.html', {'datosform': datosform})

#def DatosTecnico(request):
    if request.method == 'POST':
        datosform = DatosTecnicoForm(request.POST)
        if datosform.is_valid():
            if request.user.is_authenticated:
                # Si el usuario está autenticado, guarda los datos del administrador
                datos_tecnico = datosform.save(commit=False)
                datos_tecnico.usuario = request.user
                datos_tecnico.save()
                return redirect('reportes')  # Reemplaza 'reportes' con la URL a la que deseas redirigir después de guardar los datos
            else:
                # Si el usuario no está autenticado, puedes guardar los datos en una sesión temporal
                request.session['datos_tecnico_temp'] = datosform.cleaned_data
                return redirect('registrar')  # Redirigir al usuario a la página de inicio de sesión
    else:
        datosform = DatosTecnicoForm()
    return render(request, 'datos_tecnico.html', {'datosform': datosform})

def isesion(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Intentar autenticar con el nombre de usuario
            usuario = authenticate(request=request, username=username, password=password)

            # Si la autenticación con el nombre de usuario falla, intentar con el correo electrónico
            if usuario is None:
                UsuarioModel = get_user_model()
                try:
                    usuario = UsuarioModel.objects.get(email=username)
                    usuario = authenticate(request=request, username=usuario.username, password=password)
                except UsuarioModel.DoesNotExist:
                    pass

            if usuario is not None:
                login(request, usuario)
                return redirect('reportes')  # Redirigir a la página de inicio después del inicio de sesión exitoso
        else:
            error_message = 'Error al iniciar sesión. Por favor, verifica tus credenciales.'
            return render(request, 'isesion.html', {'isesionform': form, 'error_message': error_message})
    else:
        form = CustomAuthenticationForm()
    return render(request, 'isesion.html', {'isesionform': form})

def modificar_datos(request):
    usuario = request.user
    try:
        datos_usuario = usuario.perfilusuario
    except PerfilUsuario.DoesNotExist:
        datos_usuario = None

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=datos_usuario)
        if form.is_valid():
            datos_usuario = form.save(commit=False)
            datos_usuario.usuario = request.user
            datos_usuario.save()
            return redirect('reportes')  # Reemplaza 'reportes' con la URL a la que deseas redirigir después de guardar los datos
    else:
        form = PerfilForm(instance=datos_usuario)






def csesion(request):
    logout(request)
    return redirect('inicio')

