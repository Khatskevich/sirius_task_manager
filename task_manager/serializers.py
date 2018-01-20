from rest_framework import serializers

from core.serializers import UserSerializer

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
