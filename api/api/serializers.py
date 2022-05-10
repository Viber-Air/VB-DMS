from rest_framework import serializers
from .models import Module, RawData, DataBatch

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'

class RawDataSerializer(serializers.ModelSerializer):
    module = serializers.PrimaryKeyRelatedField(queryset=Module.objects.all())
    class Meta:
        model = RawData
        fields = '__all__'
        depth = 1


class DataBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataBatch
        fields = '__all__'
        depth = 1
