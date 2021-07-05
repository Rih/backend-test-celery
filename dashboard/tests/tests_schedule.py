# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# # Standard libs
import uuid
# # Django libs
from django.test import TestCase, tag
# # Own libs
from dashboard.models import Menu, Meal
from backend_test.tasks import schedule_menu_process


@tag('scheduler')
class ScheduleTest(TestCase):

    fixtures = [
        'meal',
        'order',
        'site'
    ]

    @tag('schedule_postsave')
    def tests_schedule_postsave(self):
        # python manage.py test --tag=schedule_postsave
        meals = Meal.objects.all()
        menu = Menu.objects.create(
            pk=str(uuid.uuid4()),
        )
        for m in meals:
            menu.meals.add(m)
        # menu = Menu.objects.last()
        print(meals)
        # for m in meals:
        #    menu.meals.add(m)
        for mm in menu.meals.all():
            print(mm)
        schedule_menu_process(menu)
