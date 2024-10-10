from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import LimitOffsetPagination

from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer
from .permissions import IsCompletedAdmin, ReadOnly


# ListAPIView, CeateAPIView, RetrieveAPIView, UpdateAPIView, DestryAPIView

class TaskViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsCompletedAdmin, ReadOnly]
    authentication_classes = [
        BasicAuthentication, SessionAuthentication,
    ]
    lookup_field = 'id'
    pagination_class = LimitOffsetPagination
    filterset_fields = ('completed', 'category__name')


# or ReadOnlyModelViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    pagination_class = None
