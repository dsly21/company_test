from django_filters import OrderingFilter
from django_filters.rest_framework import FilterSet

from company_api.models import Department


class DepartmentOrderingFilter(FilterSet):
    average_salary = OrderingFilter(
        fields=('average_salary', )
        )

    class Meta:
        model = Department
        fields = ('average_salary', )



