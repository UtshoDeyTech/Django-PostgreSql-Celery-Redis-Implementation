from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = ['id', 'status', 'task_name', 'created_at', 'updated_at', 
                  'input_data', 'result', 'progress', 'related_table', 
                  'related_id', 'operation']
    
    def get_progress(self, obj):
        return obj.get_progress()

class TaskListSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = ['id', 'status', 'task_name', 'created_at', 'updated_at', 
                 'progress', 'related_table', 'related_id', 'operation']
    
    def get_progress(self, obj):
        return obj.get_progress()