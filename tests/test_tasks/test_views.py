import logging

import pytest
from django.urls import reverse
from django.utils import timezone

from tasks.models import Task


logging.basicConfig(filename='myapp.log')
logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_category_list_views(api_client, categories_data):
    url = reverse('tasks:category-list')

    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 10
    logger.info("Response list api endpoint :")
    logger.info(str(response.data))
    assert "Test category 0" == response.data[0]['name']
    assert [] == response.data[0]['tasks']


@pytest.mark.django_db
def test_task_list_views_unauthenticated_user(api_client):
    url = reverse('tasks:task-list')
    response = api_client.get(url)
    logger.debug("Message test list views")
    assert response.status_code == 401
    assert response.data['detail'] == (
        "Informations d'authentification non fournies."
    )


@pytest.mark.django_db
def test_task_list_views_wrong_unauthenticated_user(api_client):
    url = reverse('tasks:task-list')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer inalfjalkjkfa')
    response = api_client.get(url)
    logger.error("Error test logger")
    assert response.status_code == 401


@pytest.mark.django_db
def test_task_list_view_with_authenticated_user(authenticated_user_api_client):
    authenticated_api_client, user = authenticated_user_api_client
    url = reverse('tasks:task-list')
    response = authenticated_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data['results']) == 0
    assert response.data['results'] == []


@pytest.mark.django_db
def test_delete_task_view(authenticated_user_api_client):
    authenticated_api_client, user = authenticated_user_api_client
    instance = Task.objects.create(
        name='Title task delete',
        description='Description task delete',
        expired_at=timezone.now(),
        owner=user,
    )
    url = f'/api/tasks/{instance.pk}/'
    assert Task.objects.filter(pk=instance.pk).exists()

    response = authenticated_api_client.delete(url)

    assert response.status_code == 204
    assert not Task.objects.filter(name='Title task delete').exists()
