from rest_framework import serializers
from .models import DatosUsuario


class DatosUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosUsuario
        fields = '__all__'
