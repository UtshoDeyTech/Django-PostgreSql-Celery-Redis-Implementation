import time
import random
from celery import shared_task
from celery.utils.log import get_task_logger
from .models import User
from celery_worker_app.models import Task

logger = get_task_logger(__name__)

@shared_task(bind=True)
def create_user(self, user_data):
    """
    Celery task to create a user asynchronously
    """
    task_id = self.request.id
    logger.info(f"Task {task_id} STARTED: Creating user {user_data['username']}")
    
    try:
        # Update task state in database
        task = Task.objects.get(id=task_id)
        task.status = "PROCESSING"
        task.set_progress(0)
        task.save()
        
        # Simulate a time-consuming operation
        total_steps = 5
        for step in range(1, total_steps + 1):
            # Sleep for a random time to simulate processing
            time.sleep(random.uniform(1.0, 2.0))
            
            # Update progress
            progress = int((step / total_steps) * 100)
            task.set_progress(progress)
            
            # Update Celery task meta
            self.update_state(
                state="PROGRESS",
                meta={"progress": progress}
            )
            
            logger.info(f"Task {task_id} progress: {progress}%")
        
        # Create the user
        user = User.objects.create(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
            is_active=user_data.get('is_active', True),
        )
        
        # Update task with success result
        task.status = "DONE"
        task.result = {
            "success": True,
            "user_id": str(user.id),
            "message": f"Successfully created user {user.username}",
            "progress": 100
        }
        task.save()
        
        return task.result
        
    except Exception as e:
        logger.error(f"Task {task_id} FAILED with error: {str(e)}")
        
        # Update task with error
        try:
            task = Task.objects.get(id=task_id)
            task.status = "FAILED"
            task.result = {"error": str(e), "progress": 0}
            task.save()
        except Exception as inner_e:
            logger.error(f"Failed to update task status: {str(inner_e)}")
            
        raise

@shared_task(bind=True)
def update_user(self, user_id, user_data):
    """
    Celery task to update a user asynchronously
    """
    task_id = self.request.id
    logger.info(f"Task {task_id} STARTED: Updating user {user_id}")
    
    try:
        # Update task state in database
        task = Task.objects.get(id=task_id)
        task.status = "PROCESSING"
        task.set_progress(0)
        task.save()
        
        # Simulate a time-consuming operation
        total_steps = 4
        for step in range(1, total_steps + 1):
            # Sleep for a random time to simulate processing
            time.sleep(random.uniform(0.5, 1.5))
            
            # Update progress
            progress = int((step / total_steps) * 100)
            task.set_progress(progress)
            
            # Update Celery task meta
            self.update_state(
                state="PROGRESS",
                meta={"progress": progress}
            )
            
            logger.info(f"Task {task_id} progress: {progress}%")
        
        # Get and update the user
        try:
            user = User.objects.get(id=user_id)
            
            if 'username' in user_data:
                user.username = user_data['username']
            if 'email' in user_data:
                user.email = user_data['email']
            if 'first_name' in user_data:
                user.first_name = user_data['first_name']
            if 'last_name' in user_data:
                user.last_name = user_data['last_name']
            if 'is_active' in user_data:
                user.is_active = user_data['is_active']
                
            user.save()
            
            # Update task with success result
            task.status = "DONE"
            task.result = {
                "success": True,
                "user_id": str(user.id),
                "message": f"Successfully updated user {user.username}",
                "progress": 100
            }
            task.save()
            
            return task.result
            
        except User.DoesNotExist:
            error = f"User with ID {user_id} does not exist"
            task.status = "FAILED"
            task.result = {"error": error, "progress": 0}
            task.save()
            raise Exception(error)
        
    except Exception as e:
        logger.error(f"Task {task_id} FAILED with error: {str(e)}")
        
        # Update task with error
        try:
            task = Task.objects.get(id=task_id)
            task.status = "FAILED"
            task.result = {"error": str(e), "progress": 0}
            task.save()
        except Exception as inner_e:
            logger.error(f"Failed to update task status: {str(inner_e)}")
            
        raise

@shared_task(bind=True)
def delete_user(self, user_id):
    """
    Celery task to delete a user asynchronously
    """
    task_id = self.request.id
    logger.info(f"Task {task_id} STARTED: Deleting user {user_id}")
    
    try:
        # Update task state in database
        task = Task.objects.get(id=task_id)
        task.status = "PROCESSING"
        task.set_progress(0)
        task.save()
        
        # Simulate a time-consuming operation
        total_steps = 3
        for step in range(1, total_steps + 1):
            # Sleep for a random time to simulate processing
            time.sleep(random.uniform(0.5, 1.0))
            
            # Update progress
            progress = int((step / total_steps) * 100)
            task.set_progress(progress)
            
            # Update Celery task meta
            self.update_state(
                state="PROGRESS",
                meta={"progress": progress}
            )
            
            logger.info(f"Task {task_id} progress: {progress}%")
        
        # Get and delete the user
        try:
            user = User.objects.get(id=user_id)
            username = user.username
            user.delete()
            
            # Update task with success result
            task.status = "DONE"
            task.result = {
                "success": True,
                "message": f"Successfully deleted user {username}",
                "progress": 100
            }
            task.save()
            
            return task.result
            
        except User.DoesNotExist:
            error = f"User with ID {user_id} does not exist"
            task.status = "FAILED"
            task.result = {"error": error, "progress": 0}
            task.save()
            raise Exception(error)
        
    except Exception as e:
        logger.error(f"Task {task_id} FAILED with error: {str(e)}")
        
        # Update task with error
        try:
            task = Task.objects.get(id=task_id)
            task.status = "FAILED"
            task.result = {"error": str(e), "progress": 0}
            task.save()
        except Exception as inner_e:
            logger.error(f"Failed to update task status: {str(inner_e)}")
            
        raise

@shared_task(bind=True)
def get_user(self, user_id):
    """
    Celery task to get a user asynchronously
    """
    task_id = self.request.id
    logger.info(f"Task {task_id} STARTED: Getting user {user_id}")
    
    try:
        # Update task state in database
        task = Task.objects.get(id=task_id)
        task.status = "PROCESSING"
        task.set_progress(0)
        task.save()
        
        # Simulate a time-consuming operation (just for demonstration)
        time.sleep(random.uniform(0.5, 1.5))
        task.set_progress(50)
        
        # Get the user
        try:
            user = User.objects.get(id=user_id)
            
            # Update task with success result
            user_data = {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_active": user.is_active,
                "date_joined": user.date_joined.isoformat()
            }
            
            task.status = "DONE"
            task.result = {
                "success": True,
                "user": user_data,
                "progress": 100
            }
            task.save()
            
            return task.result
            
        except User.DoesNotExist:
            error = f"User with ID {user_id} does not exist"
            task.status = "FAILED"
            task.result = {"error": error, "progress": 0}
            task.save()
            raise Exception(error)
        
    except Exception as e:
        logger.error(f"Task {task_id} FAILED with error: {str(e)}")
        
        # Update task with error
        try:
            task = Task.objects.get(id=task_id)
            task.status = "FAILED"
            task.result = {"error": str(e), "progress": 0}
            task.save()
        except Exception as inner_e:
            logger.error(f"Failed to update task status: {str(inner_e)}")
            
        raise

@shared_task(bind=True)
def list_users(self):
    """
    Celery task to list all users asynchronously
    """
    task_id = self.request.id
    logger.info(f"Task {task_id} STARTED: Listing all users")
    
    try:
        # Update task state in database
        task = Task.objects.get(id=task_id)
        task.status = "PROCESSING"
        task.set_progress(0)
        task.save()
        
        # Simulate a time-consuming operation
        time.sleep(random.uniform(1.0, 2.0))
        task.set_progress(50)
        
        # Get all users
        users = User.objects.all()
        user_list = []
        
        for user in users:
            user_list.append({
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_active": user.is_active,
                "date_joined": user.date_joined.isoformat()
            })
        
        # Update task with success result
        task.status = "DONE"
        task.result = {
            "success": True,
            "users": user_list,
            "count": len(user_list),
            "progress": 100
        }
        task.save()
        
        return task.result
        
    except Exception as e:
        logger.error(f"Task {task_id} FAILED with error: {str(e)}")
        
        # Update task with error
        try:
            task = Task.objects.get(id=task_id)
            task.status = "FAILED"
            task.result = {"error": str(e), "progress": 0}
            task.save()
        except Exception as inner_e:
            logger.error(f"Failed to update task status: {str(inner_e)}")
            
        raise