from django.contrib import admin
from .models import Administrador, Tecnico

@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'rol', 'is_active', 'date_joined')
    list_filter = ('rol', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    
@admin.register(Tecnico)
class TecnicoAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'rol', 'is_active', 'date_joined')
    list_filter = ('rol', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
