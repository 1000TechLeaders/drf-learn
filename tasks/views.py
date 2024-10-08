from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer


# ListAPIView, CeateAPIView, RetrieveAPIView, UpdateAPIView, DestryAPIView

class TaskViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [
        BasicAuthentication, SessionAuthentication,
    ]
    lookup_field = 'id'


# or ReadOnlyModelViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
