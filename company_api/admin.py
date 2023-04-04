from django.contrib import admin
from .models import Employee, Department


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'salary', 'age', 'department')
    search_fields = ('full_name', 'id')


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'director')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department, DepartmentAdmin)
