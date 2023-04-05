from django.contrib import admin
from django.db.models import Value
from django.db.models.functions import Concat

from .models import Employee, Department


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'salary', 'age', 'department')
    search_fields = ('full_name', 'id')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            full_name=Concat(
                'name', Value(' '),
                'surname', Value(' '),
                'middle_name', Value(' ')
            )
        )
        return queryset

    def full_name(self, obj):
        return f'{obj.name} {obj.surname} {obj.middle_name}'


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'director')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department, DepartmentAdmin)
