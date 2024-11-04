from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from tasks.serializers import TaskSerializer
from tasks.models import Task, Category


class TaskSerializerTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Category 1')
        self.task = Task.objects.create(
            name='Task 1', description='description 1',
            category=self.category, expired_at=timezone.now()
        )
        self.data = {
            'name': 'Task test',
            'description': 'Task description test',
             "category": {
                "name": "category test"
             },
            'created_at': timezone.now() + timedelta(days=1),
            'expired_at': timezone.now() + timedelta(days=5)
        }

    def test_validate_level_with_invalid_data(self):
        self.data['level'] = 11
        serializer = TaskSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertIn('level', serializer.errors)
        self.assertEqual(
            serializer.errors['level'][0],
            "Le niveau doit etre compris entre 0 et 10"
        )

    def test_validate_name_with_invalid_data(self):
        self.data['name'] = 'Task 1'
        serializer = TaskSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertIn('name', serializer.errors)
        self.assertEqual(
            serializer.errors['name'][0],
            "Nom de tache unique"
        )

    def test_validate_date_with_invalid_data(self):
        self.data['created_at'] = timezone.now() + timedelta(days=2)
        self.data['expired_at'] = timezone.now() + timedelta(days=1)
        serializer = TaskSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertIn(
            "La date d'expiration doit etre superieur a la date creation",
            serializer.errors['non_field_errors']
        )

    def test_serializer_with_valid_data(self):
        serializer = TaskSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), True)
        task = serializer.save()
        self.assertEqual(Task.objects.filter(name=self.data['name']).exists(), True)

    def test_serializer_update_with_valid_data(self):
        update_data = {
            'name': "New Name",
            "description": "New description"
        }
        serializer = TaskSerializer(
            instance=self.task, data=update_data, partial=True
        )
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'New Name')
        self.assertEqual(self.task.description, 'New description')
