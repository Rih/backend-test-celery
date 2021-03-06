# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# # Standard libs
from datetime import datetime as dt
# # Django libs
from django.test import TestCase, tag
# # Own libs
from dashboard.models import Meal
from dashboard.factories import MenuFactory
from backend_test.tasks import schedule_menu_process
from unittest.mock import patch
from dashboard.tests.mock import RequestMock


@tag('scheduler')
class ScheduleTest(TestCase):

    fixtures = [
        'user',
        'meal',
        'order',
        'site'
    ]

    @tag('schedule_postsave')
    @patch('requests.post')
    def tests_schedule_postsave(self, request_mock):
        # python manage.py test --tag=schedule_postsave
        request_mock.return_value = RequestMock(mode='success')
        meals = Meal.objects.all()
        menu = MenuFactory(
            scheduled_at=dt.utcnow().date(),
            meals=[1, 2],
        )
        for m in meals:
            menu.meals.add(m)
        # menu = Menu.objects.last()
        print(meals)
        # for m in meals:
        #    menu.meals.add(m)
        for mm in menu.meals.all():
            print(mm)
        res = schedule_menu_process(menu.id)
        self.assertTrue(res['result']['ok'])
