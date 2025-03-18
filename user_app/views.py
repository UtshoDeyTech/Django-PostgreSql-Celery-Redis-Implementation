from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import UserSerializer
from .tasks import create_user, update_user, delete_user, get_user, list_users
from celery_worker_app.models import Task

class UserViewSet(viewsets.ViewSet):
    """
    A viewset that provides CRUD operations for users through Celery tasks
    """
    
    def list(self, request):
        """
        List all users by creating a Celery task
        """
        # Create a Celery task
        task_result = list_users.delay()
        
        # Create a task record in the database
        task = Task.objects.create(
            id=task_result.id,
            status="PENDING",
            task_name="list_users",
            related_table="user",
            operation="READ",
            input_data={},
            result={"progress": 0}
        )
        
        return Response({
            "task_id": task.id,
            "message": "Task created to list all users",
            "status_endpoint": f"/api/tasks/{task.id}/status/"
        }, status=status.HTTP_202_ACCEPTED)
    
    def retrieve(self, request, pk=None):
        """
        Retrieve a user by creating a Celery task
        """
        # Create a Celery task
        task_result = get_user.delay(pk)
        
        # Create a task record in the database
        task = Task.objects.create(
            id=task_result.id,
            status="PENDING",
            task_name="get_user",
            related_table="user",
            related_id=pk,
            operation="READ",
            input_data={"user_id": pk},
            result={"progress": 0}
        )
        
        return Response({
            "task_id": task.id,
            "message": f"Task created to retrieve user {pk}",
            "status_endpoint": f"/api/tasks/{task.id}/status/"
        }, status=status.HTTP_202_ACCEPTED)
    
    def create(self, request):
        """
        Create a user by creating a Celery task
        """
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a Celery task
        task_result = create_user.delay(serializer.validated_data)
        
        # Create a task record in the database
        task = Task.objects.create(
            id=task_result.id,
            status="PENDING",
            task_name="create_user",
            related_table="user",
            operation="CREATE",
            input_data=serializer.validated_data,
            result={"progress": 0}
        )
        
        return Response({
            "task_id": task.id,
            "message": f"Task created to create user {serializer.validated_data['username']}",
            "status_endpoint": f"/api/tasks/{task.id}/status/"
        }, status=status.HTTP_202_ACCEPTED)
    
    def update(self, request, pk=None):
        """
        Update a user by creating a Celery task
        """
        serializer = UserSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a Celery task
        task_result = update_user.delay(pk, serializer.validated_data)
        
        # Create a task record in the database
        task = Task.objects.create(
            id=task_result.id,
            status="PENDING",
            task_name="update_user",
            related_table="user",
            related_id=pk,
            operation="UPDATE",
            input_data={"user_id": pk, "data": serializer.validated_data},
            result={"progress": 0}
        )
        
        return Response({
            "task_id": task.id,
            "message": f"Task created to update user {pk}",
            "status_endpoint": f"/api/tasks/{task.id}/status/"
        }, status=status.HTTP_202_ACCEPTED)
    
    def partial_update(self, request, pk=None):
        """
        Partially update a user by creating a Celery task
        """
        # This just calls the update method since it already handles partial updates
        return self.update(request, pk)
    
    def destroy(self, request, pk=None):
        """
        Delete a user by creating a Celery task
        """
        # Create a Celery task
        task_result = delete_user.delay(pk)
        
        # Create a task record in the database
        task = Task.objects.create(
            id=task_result.id,
            status="PENDING",
            task_name="delete_user",
            related_table="user",
            related_id=pk,
            operation="DELETE",
            input_data={"user_id": pk},
            result={"progress": 0}
        )
        
        return Response({
            "task_id": task.id,
            "message": f"Task created to delete user {pk}",
            "status_endpoint": f"/api/tasks/{task.id}/status/"
        }, status=status.HTTP_202_ACCEPTED)