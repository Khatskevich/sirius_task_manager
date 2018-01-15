from rest_framework import serializers

from core.serializers import UserSerializer

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    access_list = UserSerializer(read_only=True, many=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'end_time', 'owner', 'access_list')

