from rest_framework import serializers

from core.serializers import UserSerializer

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        read_only_fields = ("owner", "id", "created_at")
        fields = '__all__'
