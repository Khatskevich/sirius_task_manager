from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets, decorators, permissions, status
from rest_framework.decorators import list_route
from rest_framework.response import Response

from .serializers import TaskSerializer
from .models import Task

USER_MODEL = get_user_model()


# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Task.objects.all().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @list_route(methods=["get"])
    def wall(self, request):
        user = request.user
        queryset = Task.objects.filter(owner__in=user.subscribed_on.all())
        return Response(self.serializer_class(queryset, many=True).data, status.HTTP_200_OK)