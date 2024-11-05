import pytest
from rest_framework.test import APIClient
from tasks.models import Category
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken


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
def authenticated_api_client(api_client):
    user = User.objects.create_user(
        email='testuser@gmail.com',
        username='testuser@gmail.com',
        password='123245',
        is_superuser=True
    )
    token = AccessToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')
    return api_client
