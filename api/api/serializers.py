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
