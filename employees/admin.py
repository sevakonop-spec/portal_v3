from django.contrib import admin
from .models import Department, EmployeeProfile


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'order']
    list_editable = ['order']
    search_fields = ['name']
    list_select_related = ['parent']


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'job_title', 'department', 'phone', 'is_manager']
    list_filter = ['department', 'is_manager']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'job_title']
    raw_id_fields = ['user']
    list_select_related = ['user', 'department']