from rest_framework import serializers
from .models import RawData, DataBatch

class RawDataSerializer(serializers.ModelSerializer):
    measures = serializers.JSONField()
    class Meta:
        model = RawData
        fields = '__all__'


class DataBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataBatch
        fields = '__all__'
        depth = 2
