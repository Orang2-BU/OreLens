from rest_framework import serializers
from .models import RawDataLog, NormalizedMetric, DataAuditItem


class RawDataLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawDataLog
        fields = '__all__'


class NormalizedMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormalizedMetric
        fields = '__all__'


class DataAuditItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataAuditItem
        fields = '__all__'
