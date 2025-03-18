from django.db import models
import uuid

class User(models.Model):
    """
    Custom User model (separate from Django's auth User)
    This is just an example model for CRUD operations
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ['-date_joined']