from rest_framework import serializers
from .models import Commodity, CommodityPriceSeries, CommodityDriver


class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = '__all__'


class CommodityPriceSeriesSerializer(serializers.ModelSerializer):
    commodity_code = serializers.CharField(source='commodity.code', read_only=True)

    class Meta:
        model = CommodityPriceSeries
        fields = '__all__'


class CommodityDriverSerializer(serializers.ModelSerializer):
    commodity_code = serializers.CharField(source='commodity.code', read_only=True)

    class Meta:
        model = CommodityDriver
        fields = '__all__'
