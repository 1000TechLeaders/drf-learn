from django.test import TestCase
from django.utils import timezone

from tasks.models import Category, Task


class CategoryTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Category 1')
        self.task1 = Task.objects.create(
            name='Task 1', description='description 1',
            category=self.category, expired_at=timezone.now()
        )


    def test_task_level_default_value(self):
        self.assertEqual(self.task1.level, 0)
        self.assertEqual(self.task1.completed, False)


    def test_task_is_editable(self):
        self.task1.completed = False
        self.task1.save()
        self.assertEqual(self.task1.is_editable, True)

        self.task1.completed = True
        self.task1.save()

        self.assertEqual(self.task1.is_editable, False)
