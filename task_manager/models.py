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
    finish_date = models.DateField(null=True, blank=True)
    finish_time = models.TimeField(null=True, blank=True)
    repeat_settings = models.CharField(max_length=20, null=True, blank=True)


class Like(models.Model):
    user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        # User cannot like task twice
        unique_together = (("user", "task"),)
