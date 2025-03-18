from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from celery.result import AsyncResult
from .models import Task
from .serializers import TaskSerializer, TaskListSerializer

class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset that provides only read actions for tasks.
    Create actions are handled by individual apps.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializer
        return TaskSerializer
    
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """
        Get the status of a task
        """
        try:
            task = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get the latest status from Celery
        task_result = AsyncResult(pk)
        
        # Update the task status in the database if it has changed
        celery_status = task_result.status
        if task.status != celery_status:
            if celery_status == "PENDING":
                task.status = "PENDING"
            elif celery_status == "STARTED":
                task.status = "PROCESSING"
            elif celery_status == "SUCCESS":
                task.status = "DONE"
                if task_result.ready():
                    task.result = task_result.get()
            else:
                task.status = celery_status
                
            task.save()
        
        # Prepare the response
        serializer = TaskSerializer(task)
        return Response(serializer.data)