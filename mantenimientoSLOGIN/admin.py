from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import SuperUsuario, Administrador, Tecnico

# Personalizar el formulario de cambio de usuario para el SuperUsuario
class SuperUsuarioChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = SuperUsuario

# Personalizar el formulario de creación de usuario para el SuperUsuario
class SuperUsuarioCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = SuperUsuario

# Personalizar la visualización y los campos del modelo SuperUsuario en el panel de administración
class SuperUsuarioAdmin(UserAdmin):
    form = SuperUsuarioChangeForm
    add_form = SuperUsuarioCreationForm

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('campo_adicional1', 'campo_adicional2',)}),
    )

class AdministradorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'telefono']  # Campos a mostrar en la lista de administradores
    search_fields = ['nombre', 'email']  # Campos por los que se puede buscar en el panel de administración
    list_filter = ['activo']  # Filtros disponibles en la lista de administradores
    ordering = ['nombre']  # Orden de los administradores en la lista
    # ...


class TecnicoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'especialidad', 'activo']  # Campos a mostrar en la lista de técnicos
    search_fields = ['nombre', 'especialidad']  # Campos por los que se puede buscar en el panel de administración
    list_filter = ['activo', 'especialidad']  # Filtros disponibles en la lista de técnicos
    ordering = ['nombre']  # Orden de los técnicos en la lista
    # ...
# Registrar los modelos en el panel de administración
admin.site.register(SuperUsuario, SuperUsuarioAdmin)
admin.site.register(Administrador, AdministradorAdmin)
admin.site.register(Tecnico, TecnicoAdmin)