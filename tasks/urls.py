from django.urls import path

from .views import ListCreateTaskView, DetailDeleteTaskView

urlpatterns = [
    path('tasks', ListCreateTaskView.as_view()),
    path('tasks/<int:pk>', DetailDeleteTaskView.as_view()),
]
