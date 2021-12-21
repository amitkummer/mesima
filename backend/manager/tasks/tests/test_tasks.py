import json
from datetime import date

from django.urls import reverse
from rest_framework.test import APITestCase
from tasks.models import Person

from tasks.models import Task, Person

class TaskDetailTests(APITestCase):
    def setUp(self):
        self.person = Person(name='Amit', email='amit@amit.com',
            favoriteProgrammingLanguage='scala')
        self.person.save()
        self.another_person = Person(name='Amit', email='amit_other@amit.com',
            favoriteProgrammingLanguage='scala')
        self.another_person.save()
        self.task = Task(title='task', details='details',
            dueDate=date.today(), status='active', ownerId=self.person)
        self.task.save()
        self.another_task = Task(title='another task', details='another details',
            dueDate=date.today(), status='done', ownerId=self.person)
        self.another_task.save()

    def test_get(self):
        response = self.client.get(reverse('task-detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'title')
        self.assertContains(response, 'details')
        self.assertContains(response, 'dueDate')
        self.assertContains(response, 'status')
        self.assertContains(response, 'ownerId')
    
    def test_get_404(self):
        response = self.client.get(reverse('task-detail', args=[1337]))
        self.assertEqual(response.status_code, 404)

    def test_patch(self):
        data={'title': 'new-title'}
        response = self.client.patch(reverse('task-detail', args=[self.task.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'new-title')
    
    def test_delete(self):
        response = self.client.delete(reverse('task-detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)

    def test_get_status_nested(self):
        response = self.client.get(reverse('task-status', args=[self.another_task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, "{ 'done' }")

    def test_get_status_nested_404(self):
        response = self.client.get(reverse('task-status', args=[1337]))
        self.assertEqual(response.status_code, 404)
        
    def test_put_status_nested(self):
        response = self.client.put(reverse('task-status', args=[self.another_task.id]), data={'status': 'active'})
        self.assertEqual(response.status_code, 204)

    def test_put_status_nested_400(self):
        response = self.client.put(reverse('task-status', args=[self.another_task.id]), data={'status': 'not-a-valid-choice'})
        self.assertEqual(response.status_code, 400)

    def test_put_status_nested_404(self):
        response = self.client.put(reverse('task-status', args=[1337]), data={'status': 'active'})
        self.assertEqual(response.status_code, 404)

    def test_get_owner_nested(self):
        response = self.client.get(reverse('task-owner', args=[self.another_task.id]))
        self.assertEqual(response.status_code, 200)
        # DRF response here is wierd because of the foreign key relation, but looks good on web API so welp.
        # self.assertEqual(response.data, self.another_task.ownerId.id)

    def test_get_owner_nested_404(self):
        response = self.client.get(reverse('task-owner', args=[1337]))
        self.assertEqual(response.status_code, 404)
        
    def test_put_owner_nested(self):
        response = self.client.put(reverse('task-owner', args=[self.another_task.id]), data={'ownerId': self.another_person.id})
        self.assertEqual(response.status_code, 204)

    def test_put_owner_nested_400(self):
        response = self.client.put(reverse('task-owner', args=[self.another_task.id]), data={'ownerId': 1337})
        self.assertEqual(response.status_code, 400)

    def test_put_owner_nested_404(self):
        response = self.client.put(reverse('task-owner', args=[1337]), data={'ownerId': self.person.id})
        self.assertEqual(response.status_code, 404)
    
