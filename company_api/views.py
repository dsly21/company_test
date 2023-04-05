from django.db.models import Count, Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.response import Response

from .filters import DepartmentOrderingFilter
from .models import Department, Employee
from .paginators import StandardResultsPagination
from .permissions import IsSuperUserOrReadOnlyPermission
from .serializers import (
    DepartmentSerializer,
    EmployeeSerializer
)


class EmployeeViewSet(viewsets.ModelViewSet):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthenticated
    ]

    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'full_name',
        'id'
    ]


class DepartmentViewSet(viewsets.ModelViewSet):

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsSuperUserOrReadOnlyPermission
    ]

    filterset_class = DepartmentOrderingFilter

    def get_queryset(self):
        return Department.objects.annotate(
            employees_count=Count('employees'),
            average_salary=Avg('employees__salary'),
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer_data = serializer.data

        serializer_data['employees'] = EmployeeSerializer(
            instance.employees
            .exclude(id=instance.director_id), many=True
        ).data

        return Response(serializer_data)
