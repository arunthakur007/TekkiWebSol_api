from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Add custom fields here, if needed

    def __str__(self):
        return self.username
    
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, default='Todo')
    members = models.ManyToManyField(User, related_name='tasks')

    def __str__(self):
        return self.title    