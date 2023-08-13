from rest_framework import serializers
from .models import Reportes

class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reportes
        fields = '__all__'
