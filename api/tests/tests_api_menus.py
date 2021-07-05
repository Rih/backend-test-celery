# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
# # Standard libs
import uuid
import json
# # Django libs
from django.urls import reverse
from django.utils import timezone
from unittest.mock import patch
from django.test import TestCase, tag, override_settings
# from rest_framework.test import APITestCase, APIClient
# # Own libs
from dashboard.models import Menu, Meal
from account.factories import UserFactory
from dashboard.factories import MenuFactory, MealFactory


@tag('api_menus')
@override_settings(
)
class ApiMenuTest(TestCase):
    fixtures = [
        'meal',
        'menu',
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
    
    @tag('api_menu_list')
    def tests_api_menu_list(self):
        # python manage.py test --tag=api_menu_list
        url = reverse('api:menu_list_action-list')
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
            ['id', 'meals', 'scheduled_at']
        )
    
    @tag('api_menu_delete')
    def tests_api_menu_delete(self):
        # python manage.py test --tag=api_menu_delete
        a_menu = MenuFactory()
        a_menu.save()
        url = reverse('api:menus_action-detail', kwargs={'pk': a_menu.id})
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
        menu = Menu.objects.filter(id=a_menu.id).last()
        self.assertTrue(not (menu.deleted_at is None))


@override_settings(
)
class ApiMenuCreateTest(TestCase):
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
   
    @tag('api_menu_create')
    def tests_api_menu_create(self):
        # python manage.py test --tag=api_menu_create
        meals = [MealFactory(title=f'opcion {m + 1}') for m in range(5)]
        # schedule = timezone.now().strftime("%Y-%m-%d")
        url = reverse('api:menus_action-list')
        payload = {
            'meals': [m.id for m in meals],
            'scheduled_at': '2021-07-04'
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
            ['id', 'scheduled_at', 'created_at', 'deleted_at', 'meals']
        )
        self.assertEquals(len(result['id']), 36)
        self.assertEquals(result['scheduled_at'], '2021-07-04')
        payload['scheduled_at'] = ''
        res = self.client.post(
            url,
            json.dumps(payload),
            content_type='application/json'
        )
        result = json.loads(res.content)
        # fail required case
        self.assertEquals(res.status_code, 400)
        self.assertListEqual(
            result['scheduled_at'],
            [
                'Date has wrong format. Use one of these formats instead: YYYY-MM-DD.']
        )