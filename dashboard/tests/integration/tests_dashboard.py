# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
# # Standard libs
# # Django libs
from django.urls import reverse
from django.test import TestCase, tag
# # Own libs
from account.factories import UserFactory


@tag('dashboard')
class DashboardTest(TestCase):

    fixtures = [
        'user',
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
            f'{url}?model=meal&mode=create',
            content_type='application/html'
        )
        self.assertEquals(result.status_code, 200)
        self.assertContains(result, 'id="meal_form"')
        self.assertContains(result, 'id="meal_modal"')
        self.assertContains(result, 'New Meal')

    @tag('meal_partial_modal_edit_template')
    def tests_meal_modal_edit(self):
        # python manage.py test --tag=meal_partial_modal_edit_template
        url = reverse('dashboard:meals_edit', kwargs={
            'pk': 1
        })
        self.client.login(username='jhon', password='pass')
        result = self.client.get(
            f'{url}?model=meal&mode=edit',
            content_type='application/html'
        )
        self.assertEquals(result.status_code, 200)
        self.assertContains(result, 'id="meal_form_edit"')
        self.assertContains(result, 'id="meal_modal_edit"')
        self.assertContains(result, 'Edit Meal')

    @tag('menu_partial_modal_template')
    def tests_menu_modal_create(self):
        # python manage.py test --tag=menu_partial_modal_template
        url = reverse('dashboard:menus_create')
        self.client.login(username='jhon', password='pass')
        result = self.client.get(
            f'{url}?model=menu&mode=create',
            content_type='application/html'
        )
        self.assertEquals(result.status_code, 200)
        self.assertContains(result, 'id="menu_form"')
        self.assertContains(result, 'id="menu_modal"')
        self.assertContains(result, 'New Menu')
