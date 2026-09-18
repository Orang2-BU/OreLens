from rest_framework import serializers
from .models import Company, CompanyCommodityExposure, CompanyResilience


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class CompanyCommodityExposureSerializer(serializers.ModelSerializer):
    company_ticker = serializers.CharField(source='company.ticker', read_only=True)
    commodity_code = serializers.CharField(source='commodity.code', read_only=True)

    class Meta:
        model = CompanyCommodityExposure
        fields = '__all__'


class CompanyResilienceSerializer(serializers.ModelSerializer):
    company_ticker = serializers.CharField(source='company.ticker', read_only=True)

    class Meta:
        model = CompanyResilience
        fields = '__all__'
