from rest_framework import serializers
from .models import UserProfile, Module, RawData

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class RawDataSerializer(serializers.ModelSerializer):
    measures = serializers.JSONField()
    class Meta:
        model = RawData
        fields = '__all__'

def FastRawDataSerializer(queryset):
    return [{
        '_id'        : str(rawdata.pk),
        'module'     : rawdata.module_id,
        'measures'   : rawdata.measures,
        'temperature': rawdata.temperature,
        'voltage'    : rawdata.voltage,
        'description': rawdata.description,
        'timestamp'  : rawdata.timestamp
    } for rawdata in queryset]