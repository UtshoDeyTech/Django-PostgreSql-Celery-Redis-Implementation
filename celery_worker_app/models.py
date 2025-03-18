from django.db import models
import uuid

class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('DONE', 'Done'),
        ('FAILED', 'Failed'),
    ]
    
    id = models.CharField(primary_key=True, max_length=255, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', db_index=True)
    task_name = models.CharField(max_length=255, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    input_data = models.JSONField(default=dict)
    result = models.JSONField(default=dict, null=True, blank=True)
    # Add reference to table being processed (e.g., 'user')
    related_table = models.CharField(max_length=100, blank=True, null=True)
    related_id = models.CharField(max_length=255, blank=True, null=True)
    operation = models.CharField(max_length=20, blank=True, null=True)  # CREATE, UPDATE, DELETE, READ

    def __str__(self):
        return f"{self.task_name} ({self.id})"
    
    def get_progress(self):
        if self.result and 'progress' in self.result:
            return self.result['progress']
        return 0
    
    def set_progress(self, progress):
        if not self.result:
            self.result = {}
        current_result = self.result
        current_result['progress'] = progress
        self.result = current_result
        self.save(update_fields=['result'])