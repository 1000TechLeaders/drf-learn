import pytest
from django.urls import reverse
from tasks.models import Category


@pytest.mark.django_db
def test_create_category_view(authenticated_api_client):
    url = reverse('tasks:category-list')
    data = {
        'name': "Category test 2"
    }
    response = authenticated_api_client.post(url, data)
    assert response.status_code == 201
    assert response.data['name'] == data['name']
    assert Category.objects.filter(name=data['name']).exists()


@pytest.mark.django_db
def test_update_category_view(authenticated_api_client):
    instance = Category.objects.create(name='Test update')
    url = f'/api/categories/{instance.pk}/'
    data = {
        'name': "Test update 2"
    }
    assert Category.objects.filter(name='Test update').exists()

    response = authenticated_api_client.patch(url, data)

    assert response.status_code == 200
    assert response.data['name'] == data['name']
    assert Category.objects.filter(name=data['name']).exists()
    assert not Category.objects.filter(name='Test update').exists()


@pytest.mark.django_db
def test_delete_category_view(authenticated_api_client):
    instance = Category.objects.create(name='Test update')
    url = f'/api/categories/{instance.pk}/'
    assert Category.objects.filter(name='Test update').exists()

    response = authenticated_api_client.delete(url)

    assert response.status_code == 204
    assert not Category.objects.filter(name='Test update').exists()
