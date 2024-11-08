from django.http import JsonResponse
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

from .filters import TaskFilter
from .models import Category
from .models import Task
from .permissions import IsCompletedAdmin
from .permissions import ReadOnly
from .serializers import CategorySerializer
from .serializers import TaskSerializer


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
        JWTAuthentication, BasicAuthentication, SessionAuthentication,
    ]
    lookup_field = 'id'
    pagination_class = LimitOffsetPagination
    filterset_class = TaskFilter
    search_fields = ['name', 'description', 'category__name']
    # ordering_fields = ['created_at', 'expired_at', 'level']

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)


# or ReadOnlyModelViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    pagination_class = None


def custom_404_view(request, exception=None):
    return JsonResponse({
        'detail': 'Ressource non trouve.'
    }, status=404)


def custom_500_view(request):
    return JsonResponse({
        'detail': 'Une erreur est survenue, reessayer ulterieurment.'
    }, status=500)
