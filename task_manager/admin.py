from django.contrib import admin

from .models import Task

# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    class Meta:
        fields = ('owner', 'name', 'description', 'created_at', 'end_time')