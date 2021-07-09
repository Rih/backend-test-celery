# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
# # Standard libs
from datetime import datetime as dt, timedelta
from urllib.parse import urlencode
# # Django libs
from django.urls import reverse
from django.test import TestCase, tag, override_settings
from unittest.mock import patch
# # Own libs
from dashboard.factories import MenuFactory
from dashboard.models import Menu, Meal


@tag('order_public')
class OrderTest(TestCase):

    fixtures = [
        'user',
        'meal',
        'menu',
        'order',
        'site',
    ]

    @tag('menu_public_get')
    def tests_menu_get(self):
        # python manage.py test --tag=menu_public_get
        menu = Menu.objects.get(pk=1)
        url = reverse('menu:menu_list', kwargs={
            'pk': menu.pk
        })
        result = self.client.get(
            url,
            content_type='application/html'
        )
        self.assertEquals(result.status_code, 200)
        for meal in menu.meals.all():
            self.assertContains(result, meal.title)

    @tag('menu_public_post_error_email')
    def tests_menu_post_error_email(self):
        # python manage.py test --tag=menu_public_post_error_email
        menu = Menu.objects.get(pk=1)
        url = reverse('menu:menu_list', kwargs={
            'pk': menu.pk
        })
        meal = menu.meals.all()[0]
        payload = {
            'meal': meal.pk,
            'name': 'My name',
            'email': 'Invalid Email',
            'suggestion': 'suggest',
        }
        result = self.client.post(
            url,
            urlencode(payload),
            content_type='application/x-www-form-urlencoded'
        )
        # invalid email case
        self.assertEquals(result.status_code, 200)
        # self.assertContains(result, 'Enter a valid email address.')

    @tag('menu_public_post_error_menu_invalid')
    @override_settings(
        MAX_HOUR_TO_ORDER=1,
        UTC_TZ_OFFSET=0,
    )
    @patch('dashboard.bl.utils.get_current_date')
    def tests_menu_post_error_menu_invalid(self, nowmock):
        # python manage.py test --tag=menu_public_post_error_menu_invalid
        menu = Menu.objects.get(pk=1)
        mock_time = dt.combine(
            dt.now(),
            (dt.min + timedelta(hours=9)).time()
        )
        nowmock.return_value = mock_time
        url = reverse('menu:menu_list', kwargs={
            'pk': menu.pk
        })
        meal = menu.meals.all()[0]
        payload = {
            'meal': meal.pk,
            'name': 'My name',
            'email': 'email@test.com',
            'suggestion': 'suggest',
        }
        result = self.client.post(
            url,
            urlencode(payload),
            content_type='application/x-www-form-urlencoded'
        )
        # invalid case
        self.assertEquals(result.status_code, 200)
        self.assertContains(
            result, 'Menu is from the past, are you a time traveler?'
        )

    @tag('menu_public_post_error_invalid_time')
    @override_settings(
        MAX_HOUR_TO_ORDER=1,
        UTC_TZ_OFFSET=0,
    )
    @patch('dashboard.bl.utils.get_current_date')
    def tests_menu_post_error_invalid_time(self, nowmock):
        # python manage.py test --tag=menu_public_post_error_invalid_time
        menu = Menu.objects.get(pk=1)
        mock_time = dt.combine(
            dt.now(),
            (dt.min + timedelta(hours=9)).time()
        )
        nowmock.return_value = mock_time
        url = reverse('menu:menu_list', kwargs={
            'pk': menu.pk
        })
        meal = menu.meals.all()[0]
        payload = {
            'meal': meal.pk,
            'name': 'My name',
            'email': 'email@test.com',
            'suggestion': 'suggest',
        }
        new_menu = MenuFactory(
            scheduled_at=dt.now().date(),
            meals=[1, 2],
        )
        url = reverse('menu:menu_list', kwargs={
            'pk': new_menu.pk
        })
        result = self.client.post(
            url,
            urlencode(payload),
            content_type='application/x-www-form-urlencoded'
        )
        self.assertEquals(result.status_code, 200)
        self.assertContains(
            result, 'Not a valid time'
        )

    @tag('menu_public_post_success')
    @override_settings(
        MAX_HOUR_TO_ORDER=dt.now().hour + 1
    )
    @patch('dashboard.bl.utils.get_current_date')
    def tests_menu_post_success(self, nowmock):
        # python manage.py test --tag=menu_public_post_success
        mock_time = dt.combine(
            dt.now().date(),
            (dt.min + timedelta(hours=9)).time()
        )
        nowmock.return_value = mock_time
        new_menu = MenuFactory(
            scheduled_at=dt.now().date(),
            meals=[1, 2],
        )
        url = reverse('menu:menu_list', kwargs={
            'pk': new_menu.pk
        })
        meal = Meal.objects.get(pk=1)
        payload = {
            'meal': meal.pk,
            'name': 'My name',
            'email': 'valid@email.com',
            'suggestion': 'suggest',
        }
        result = self.client.post(
            url,
            urlencode(payload),
            content_type='application/x-www-form-urlencoded'
        )
        # valid case
        self.assertEquals(result.status_code, 302)

    @tag('menu_public_done_get')
    def tests_menu_done_get(self):
        # python manage.py test --tag=menu_public_done_get
        url = reverse('menu:menu_done')
        result = self.client.get(
            url,
            content_type='application/html'
        )
        # invalid email
        self.assertEquals(result.status_code, 200)
        self.assertContains(result, 'We will inform you when your meal is ready.')
