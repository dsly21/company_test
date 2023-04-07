from django_filters import OrderingFilter, CharFilter
from django_filters.rest_framework import FilterSet

from company_api.models import Department, Employee


class DepartmentOrderingFilter(FilterSet):
    average_salary = OrderingFilter(
        fields=('average_salary', )
        )

    class Meta:
        model = Department
        fields = ('average_salary', )


class EmployeeFilterSet(FilterSet):
    full_name = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Employee
        fields = ('full_name', 'id')


