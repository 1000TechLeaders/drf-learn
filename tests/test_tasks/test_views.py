import pytest
import logging
from django.urls import reverse
from django.utils import timezone

from tasks.models import Task, Category


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
    assert response.data['detail'] == "Informations d'authentification non fournies."


@pytest.mark.django_db
def test_task_list_views_wrong_unauthenticated_user(api_client):
    url = reverse('tasks:task-list')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer inalfjalkjkfa')
    response = api_client.get(url)
    logger.error("Error test logger")
    assert response.status_code == 401


@pytest.mark.django_db
def test_task_list_views_with_authenticated_user(authenticated_api_client):
    url = reverse('tasks:task-list')
    response = authenticated_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data['results']) == 0
    assert response.data['results'] == []
