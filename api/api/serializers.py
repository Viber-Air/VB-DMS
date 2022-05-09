from rest_framework import serializers
from .models import Module, RawData

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class RawDataSerializer(serializers.ModelSerializer):
    measures = serializers.JSONField()
    class Meta:
        model = RawData
        fields = '__all__'
        depth = 1
