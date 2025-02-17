from django.contrib import admin

from .models import Category
from .models import Task


class CategoryAdmin(admin.ModelAdmin):
	pass


class TaskAdmin(admin.ModelAdmin):
	pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Task, TaskAdmin)
