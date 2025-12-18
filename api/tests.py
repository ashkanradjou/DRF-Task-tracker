from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task


class TaskAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='password123')
        self.other_user = User.objects.create_user(username='bob', password='password123')
        self.my_task = Task.objects.create(owner=self.user, title='My Task', priority=Task.HIGH)
        self.other_task = Task.objects.create(owner=self.other_user, title='Other Task')

        login_response = self.client.post(
            '/api/auth/login/', {'username': 'alice', 'password': 'password123'}, format='json'
        )
        token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    def test_list_only_returns_own_tasks(self):
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], self.my_task.title)

    def test_filter_by_priority(self):
        Task.objects.create(owner=self.user, title='Medium Task', priority=Task.MEDIUM)
        response = self.client.get('/api/tasks/', {'priority': Task.HIGH})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [task['title'] for task in response.data['results']]
        self.assertEqual(titles, ['My Task'])

    def test_cannot_access_someone_elses_task_detail(self):
        response = self.client.get(f'/api/tasks/{self.other_task.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
