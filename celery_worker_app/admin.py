from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_name', 'status', 'related_table', 'related_id', 'operation', 'created_at', 'updated_at', 'get_progress')
    list_filter = ('status', 'task_name', 'related_table', 'operation')
    search_fields = ('id', 'task_name', 'related_id')
    readonly_fields = ('id', 'created_at', 'updated_at')