from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(default=timezone.now)


class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom de la tache")
    description = models.TextField(max_length=500)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, 
        related_name='tasks'
    )
    completed = models.BooleanField(default=False)
    level = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, related_name='tasks'
    )
    created_at = models.DateTimeField(default=timezone.now)
    expired_at = models.DateTimeField()

    @property
    def is_editable(self):
        if not self.completed:
            return True
        return False
