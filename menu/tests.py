# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
# # Standard libs
from urllib.parse import urlencode
# # Django libs
from django.urls import reverse
from django.test import TestCase, tag
# # Own libs
from dashboard.models import Menu


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

    @tag('menu_public_post')
    def tests_menu_post(self):
        # python manage.py test --tag=menu_public_post
        menu = Menu.objects.get(pk=1)
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
