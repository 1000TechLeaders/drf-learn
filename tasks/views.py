from rest_framework.viewsets import ModelViewSet
from rest_framework import generics

from .models import Task
from .serializers import TaskSerializer


class ListCreateTaskView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class DetailDeleteTaskView(generics.RetrieveDestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
