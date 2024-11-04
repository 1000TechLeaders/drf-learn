from django.urls import path
from rest_framework import routers

from .views import (
    TaskViewSet, CategoryViewSet
)

app_name = 'tasks'

router = routers.SimpleRouter()
router.register('tasks', TaskViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = router.urls
