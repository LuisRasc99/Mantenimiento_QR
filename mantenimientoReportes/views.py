from django.contrib.auth.decorators import user_passes_test,login_required
from .forms import MaquinaForm
from mantenimientoSLOGIN.models import Usuario  # Asegúrate de importar tu modelo de usuario
from .models import Maquina
from django.shortcuts import get_object_or_404, redirect, render

# Decorador para permitir solo a los administradores
@user_passes_test(lambda u: u.is_authenticated and u.tipo_usuario == 'administrador', login_url='/iniciar_sesion/')
def panel(request):
    maquinas = Maquina.objects.filter(user=request.user)
    nombre_usuario = request.user.username  # Cambia esto según tu modelo de Usuario
    context = {'maquinas': maquinas, 'nombre_usuario': nombre_usuario}
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