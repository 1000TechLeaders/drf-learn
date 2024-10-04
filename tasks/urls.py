from django.urls import path

from .views import TaskViewSet

urlpatterns = [
    path('tasks', TaskViewSet.as_view({'get': 'list', 'post': 'create'})),
]
