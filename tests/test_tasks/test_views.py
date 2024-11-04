import pytest
import logging
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from tasks.models import Task, Category
from django.contrib.auth.models import User


logger = logging.getLogger("test_views")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def categories_data():
    categories = [
        Category.objects.create(
            name=f'Test category {item}',
        )
        for item in range(10)
    ]
    return categories


@pytest.fixture
def authenticated_user(api_client):
    user = User.objects.create_user(
        email='testuser@gmail.com',
        username='testuser@gmail.com',
        password='123245',
        is_superuser=True
    )
    token = AccessToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')
    return api_client


@pytest.mark.django_db
def test_category_list_views(api_client, categories_data):
    url = reverse('tasks:category-list')

    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 10
    assert "Test category 0" == response.data[0]['name']
    assert [] == response.data[0]['tasks']


@pytest.mark.django_db
def test_task_list_views_unauthenticated_user(api_client):
    url = reverse('tasks:task-list')
    response = api_client.get(url)
    assert response.status_code == 401
    assert response.data['detail'] == "Informations d'authentification non fournies."


@pytest.mark.django_db
def test_task_list_views_with_authenticated_user(authenticated_user):
    url = reverse('tasks:task-list')
    response = authenticated_user.get(url)
    assert response.status_code == 200
    assert len(response.data['results']) == 0
    assert response.data['results'] == []
