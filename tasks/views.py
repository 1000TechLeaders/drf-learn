from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import mixins

from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer


# ListAPIView, CeateAPIView, RetrieveAPIView, UpdateAPIView, DestryAPIView

class TaskViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'

    def get_object():
        pass

    def get_queryset():
        pass


# or ReadOnlyModelViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
