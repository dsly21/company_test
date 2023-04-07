from django.db.models import (
    Count,
    Avg,
    Value,
    Subquery,
    Prefetch,
)
from django.db.models.functions import Concat
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)

from .filters import (
    DepartmentOrderingFilter,
    EmployeeFilterSet
)
from .models import Department, Employee
from .paginators import StandardResultsPagination
from .permissions import IsSuperUserOrReadOnlyPermission
from .serializers import (
    DepartmentSerializer,
    EmployeeSerializer, DepartmentListSerializer
)


class EmployeeViewSet(viewsets.ModelViewSet):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend]

    @property
    def filterset_class(self):
        if self.action == 'list':
            return EmployeeFilterSet
        return None

    def get_queryset(self):
        qs = Employee.objects.annotate(
            full_name=Concat(
                'name', Value(' '),
                'surname', Value(' '),
                'middle_name',
            )
        )
        return qs


class DepartmentViewSet(viewsets.ModelViewSet):

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    list_serializer_class = DepartmentListSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsSuperUserOrReadOnlyPermission
    ]

    filterset_class = DepartmentOrderingFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        return super().get_serializer_class()

    def get_queryset(self):
        qs = Department.objects.annotate(
            employees_count=Count('employees'),
            average_salary=Avg('employees__salary'),
        )

        if self.action == 'retrieve':
            qs = qs.prefetch_related(
                Prefetch('employees', queryset=Employee.objects
                    .exclude(
                        id__in=Subquery(qs.values('director_id'))
                    )
                )
            )
        return qs

