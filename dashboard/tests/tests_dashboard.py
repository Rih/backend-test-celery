# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
# # Standard libs
import json
# # Django libs
from django.urls import reverse
from unittest.mock import patch
from django.test import TestCase, tag
# # Own libs
from dashboard.models import Menu, Meal
from account.factories import UserFactory


@tag('dashboard')
class DashboardTest(TestCase):

    fixtures = [
        'meal',
        'menu',
        'order',
        'site',
    ]

    def setUp(self):
        ''' Check coverage
            coverage3 run --source='.' manage.py test dashboard
        '''
        self.user = UserFactory(
            username='jhon',
            email='test@ub.com',
        )
        self.user.set_password('pass')
        self.user.save()

    @tag('dashboard_index_template')
    def tests_dashboard_index(self):
        # python manage.py test --tag=dashboard_index_template
        url = reverse('dashboard:index')
        self.client.logout()
        result = self.client.get(
            url,
            content_type='application/html'
        )
        # logout case
        self.assertEquals(result.status_code, 302)
        self.client.login(username='jhon', password='pass')
        result = self.client.get(
            url,
            content_type='application/html'
        )
        # logged in case
        self.assertEquals(result.status_code, 200)
        self.assertContains(result, 'Meals')
        self.assertContains(result, 'Menus')
        self.assertContains(result, 'Orders')
        
    @tag('menu_list_template')
    def tests_menu_list(self):
        # python manage.py test --tag=menu_list_template
        url = reverse('dashboard:menus')
        self.client.logout()
        result = self.client.get(
            url,
            content_type='application/html'
        )
        # logout case
        self.assertEquals(result.status_code, 302)
        self.client.login(username='jhon', password='pass')
        result = self.client.get(
            url,
            content_type='application/html'
        )
        # logged in case
        self.assertEquals(result.status_code, 200)
        self.assertContains(result, 'My Meals')

    @tag('meal_list_template')
    def tests_meal_list(self):
        # python manage.py test --tag=meal_list_template
        url = reverse('dashboard:meals')
        self.client.logout()
        result = self.client.get(
            url,
            content_type='application/html'
        )
        # logout case
        self.assertEquals(result.status_code, 302)
        self.client.login(username='jhon', password='pass')
        result = self.client.get(
            url,
            content_type='application/html'
        )
        # logged in case
        self.assertEquals(result.status_code, 200)
        self.assertContains(result, 'My Meals')


    @tag('meal_partial_modal_template')
    def tests_meal_modal_create(self):
        # python manage.py test --tag=meal_partial_modal_template
        url = reverse('dashboard:meals_create', kwargs={
            'pk': 0
        })
        self.client.login(username='jhon', password='pass')
        result = self.client.get(
            f'{url}?model=meal',
            content_type='application/html'
        )
        self.assertEquals(result.status_code, 200)

    @tag('meal_partial_modal_edit_template')
    def tests_meal_modal_create(self):
        # python manage.py test --tag=meal_partial_modal_edit_template
        url = reverse('dashboard:meals_edit', kwargs={
            'pk': 1
        })
        self.client.login(username='jhon', password='pass')
        result = self.client.get(
            f'{url}?model=meal',
            content_type='application/html'
        )
        self.assertEquals(result.status_code, 200)
