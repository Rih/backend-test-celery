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

    @tag('menu_public_post_errors')
    @patch('dashboard.signals.current_date')
    def tests_menu_post_errors(self, nowmock):
        # python manage.py test --tag=menu_public_post_errors
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
            'email': 'My email',
            'suggestion': 'suggest',
        }
        result = self.client.post(
            url,
            urlencode(payload),
            content_type='application/x-www-form-urlencoded'
        )
        # invalid email case
        self.assertEquals(result.status_code, 200)
        self.assertContains(result, 'Enter a valid email address.')
        payload['email'] = 'email@test.com'
        result = self.client.post(
            url,
            urlencode(payload),
            content_type='application/x-www-form-urlencoded'
        )
        # invalid case
        self.assertContains(
            result, 'Menu is from the past, are you a time traveler?'
        )
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
        self.assertContains(
            result, 'Not a valid time'
        )

    @tag('menu_public_post_success')
    @override_settings(
        MAX_HOUR_TO_ORDER=dt.now().hour + 1
    )
    @patch('dashboard.signals.current_date')
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
        self.assertContains(result, 'DONE')
