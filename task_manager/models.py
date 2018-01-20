from django.contrib.auth import get_user_model
from django.db import models

USER_MODEL = get_user_model()


# Create your models here.
class Task(models.Model):
    owner = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()