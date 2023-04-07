from rest_framework import serializers

from .models import Department, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class BaseDepartmentSerializer(serializers.ModelSerializer):
    employees_count = serializers.IntegerField(read_only=True)
    average_salary = serializers.IntegerField(read_only=True)


class DepartmentSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True)

    class Meta:
        model = Department
        fields = '__all__'


class DepartmentListSerializer(BaseDepartmentSerializer):

    class Meta:
        model = Department
        fields = (
            'name',
            'director',
            'employees_count',
            'average_salary',
        )


