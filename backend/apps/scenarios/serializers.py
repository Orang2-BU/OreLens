from rest_framework import serializers
from .models import Scenario, ScenarioInput, ScenarioResult


class ScenarioInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScenarioInput
        fields = '__all__'


class ScenarioResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScenarioResult
        fields = '__all__'


class ScenarioSerializer(serializers.ModelSerializer):
    inputs = ScenarioInputSerializer(many=True, read_only=True)
    result = ScenarioResultSerializer(read_only=True)
    commodity_code = serializers.CharField(source='commodity.code', read_only=True)

    class Meta:
        model = Scenario
        fields = '__all__'
