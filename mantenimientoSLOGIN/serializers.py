from rest_framework import serializers
from .models import DatosAdministrador


class DatosAdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosAdministrador
        fields = '__all__'
