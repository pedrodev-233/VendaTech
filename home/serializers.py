from rest_framework import serializers
from .models import Product, MonthlyResult, Employee, SalesRecord


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class MonthlyResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyResult
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class SalesRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesRecord
        fields = "__all__"