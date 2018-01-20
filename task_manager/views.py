import rest_framework_filters
from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from django.shortcuts import render
from rest_framework import viewsets, decorators, permissions, status, serializers
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from .serializers import TaskSerializer
from .models import Task, Like

USER_MODEL = get_user_model()


class ExtentedTaskSerializer(TaskSerializer):
    likes_cnt = serializers.IntegerField(read_only=True)

class TaskFilter(rest_framework_filters.FilterSet):
    class Meta:
        model = Task
        fields = {
            'owner_id': ('exact',),
            'name': ('icontains',),
        }


# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = ExtentedTaskSerializer
    queryset = Task.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    filter_class = TaskFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @list_route(methods=["get"])
    def wall(self, request):
        user = request.user
        queryset = Task.objects.filter(owner__in=user.subscribed_on.all()).order_by("id")
        return Response(self.serializer_class(queryset, many=True).data, status.HTTP_200_OK)

    @detail_route(methods=["post"])
    def like(self, request, pk):
        user = request.user
        task = self.get_object()
        Like.objects.create(user=user,task=task)
        return Response("", status.HTTP_200_OK)

    @detail_route(methods=["post"])
    def unlike(self, request, pk):
        user = request.user
        task = self.get_object()
        Like.objects.filter(user=user,task=task).delete()
        return Response("", status.HTTP_200_OK)

    def get_queryset(self):
        return self.queryset.annotate(
            likes_cnt=Count('likes')
        )