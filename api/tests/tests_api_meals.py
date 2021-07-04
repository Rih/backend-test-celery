# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
# # Standard libs
import uuid
import json
# # Django libs
from django.urls import reverse
from unittest.mock import patch
from django.test import TestCase, tag, override_settings
# from rest_framework.test import APITestCase, APIClient
# # Own libs
from dashboard.models import Menu, Meal
from dashboard.bot import SlackBot, SlackReminder
from backend_test.tasks import schedule_menu_process
from account.factories import UserFactory
from dashboard.factories import MealFactory
from dashboard.tests.mock import RequestMock


@tag('api_meals')
@override_settings(
)
class ApiMealTest(TestCase):
    fixtures = [
        'meal',
        'site'
    ]
    
    def setUp(self):
        ''' Check coverage
            coverage3 run --source='.' manage.py test api
        '''
        self.user = UserFactory(
            username='jhon',
            email='test@test.com',
        )
        self.user.set_password('pass')
        self.user.save()

    @tag('api_meal_list')
    def tests_api_meal_list(self):
        # python manage.py test --tag=api_meal_list
        url = reverse('api:meals_action-list')
        self.client.login(username='jhon', password='pass')
        res = self.client.get(
            url,
            content_type='application/json'
        )
        result = json.loads(res.content)
        # success case
        self.assertEquals(res.status_code, 200)
        self.assertTrue(len(result) > 0)
        self.assertListEqual(
            list(result[0].keys()),
            ['id', 'title', 'modified_at', 'deleted_at']
        )
        
    @tag('api_meal_create')
    def tests_api_meal_create(self):
        # python manage.py test --tag=api_meal_create
        url = reverse('api:meals_action-list')
        payload = {
            'title': 'Ham with Mayo'
        }
        # logout protected
        self.client.logout()
        res = self.client.post(
            url,
            json.dumps(payload),
            content_type='application/json'
        )
        result = json.loads(res.content)
        # logout case
        self.assertEquals(res.status_code, 403)
        self.assertEquals(
            result['detail'],
            'Authentication credentials were not provided.'
        )
        self.client.login(username='jhon', password='pass')
        res = self.client.post(
            url,
            json.dumps(payload),
            content_type='application/json'
        )
        result = json.loads(res.content)
        # success case
        self.assertEquals(res.status_code, 201)
        self.assertListEqual(
            list(result.keys()),
            ['id', 'title', 'modified_at', 'deleted_at']
        )
        self.assertTrue(result['id'] > 0)
        self.assertEquals(result['title'], 'Ham with Mayo')
        payload['title'] = ''
        res = self.client.post(
            url,
            json.dumps(payload),
            content_type='application/json'
        )
        result = json.loads(res.content)
        # fail required case
        self.assertEquals(res.status_code, 400)
        self.assertListEqual(result['title'], ['This field may not be blank.'])

    @tag('api_meal_edit')
    def tests_api_meal_edit(self):
        # python manage.py test --tag=api_meal_edit
        a_meal = MealFactory()
        a_meal.save()
        url = reverse('api:meals_action-detail', kwargs={'pk': a_meal.id})
        payload = {
            'title': 'Mayo please'
        }
        # logout protected
        self.client.logout()
        res = self.client.put(
            url,
            json.dumps(payload),
            content_type='application/json'
        )
        result = json.loads(res.content)
        # logout case
        self.assertEquals(res.status_code, 403)
        self.assertEquals(
            result['detail'],
            'Authentication credentials were not provided.'
        )
        self.client.login(username='jhon', password='pass')
        res = self.client.put(
            url,
            json.dumps(payload),
            content_type='application/json'
        )
        result = json.loads(res.content)
        # success case
        self.assertEquals(res.status_code, 200)
        self.assertListEqual(
            list(result.keys()),
            ['id', 'title', 'modified_at', 'deleted_at']
        )
        self.assertEqual(result['id'], a_meal.id)
        self.assertEquals(result['title'], 'Mayo please')
        payload['title'] = ''
        res = self.client.put(
            url,
            json.dumps(payload),
            content_type='application/json'
        )
        result = json.loads(res.content)
        # fail required case
        self.assertEquals(res.status_code, 400)
        self.assertListEqual(result['title'], ['This field may not be blank.'])

    @tag('api_meal_delete')
    def tests_api_meal_delete(self):
        # python manage.py test --tag=api_meal_delete
        a_meal = MealFactory()
        a_meal.save()
        url = reverse('api:meals_action-detail', kwargs={'pk': a_meal.id})
        # logout protected
        self.client.logout()
        res = self.client.delete(
            url,
            content_type='application/json'
        )
        result = json.loads(res.content)
        # logout case
        self.assertEquals(res.status_code, 403)
        self.assertEquals(
            result['detail'],
            'Authentication credentials were not provided.'
        )
        self.client.login(username='jhon', password='pass')
        res = self.client.delete(
            url,
            content_type='application/json'
        )
        # success case
        self.assertEquals(res.status_code, 204)
        meal = Meal.objects.filter(id=a_meal.id).last()
        self.assertTrue(not(meal.deleted_at is None))

