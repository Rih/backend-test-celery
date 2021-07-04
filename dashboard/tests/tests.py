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
from dashboard.tests.mock import RequestMock


@tag('bot')
@override_settings(
)
class MealTest(TestCase):
    fixtures = [
        'site'
    ]
    
    def setUp(self):
        ''' Check coverage
            coverage3 run --source='.' manage.py test dashboard
        '''
        self.user = UserFactory(
            username='jhon',
            email='test@test.com',
        )
        self.user.set_password('pass')
        self.user.save()
    
    @tag('meal_list_template')
    def tests_meal_list(self):
        # python manage.py test --tag=meal_list_template
        url = reverse('dashboard:meals')
        payload = {
            'title': 'Ham with Mayo'
        }
        self.client.login(username='jhon', password='pass')
        result = self.client.post(
            url,
            json.dumps(payload),
            content_type='appplication/json'
        )
        result = json.loads(result)
        self.assertTrue(result)
        


@tag('bot')
@override_settings(
)
class DashboardTest(TestCase):

    fixtures = [
        'meal',
        'menu',
        'menu_meal',
        'order',
        'site'
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
    
    @tag('slackbot_send_success')
    @patch('requests.post')
    def tests_slackbot_send_success(self, request_mock):
        # python manage.py test --tag=slackbot_send_success
        request_mock.return_value = RequestMock(mode='success')
        result = SlackBot(
            CHANNEL='mock_channel'
        ).send('msg')
        self.assertTrue(result['ok'])
        
    @tag('slackbot_send_error')
    @patch('requests.post')
    def tests_slackbot_send_error(self, request_mock):
        # python manage.py test --tag=slackbot_send_success
        request_mock.return_value = RequestMock(mode='error')
        result = SlackBot(
            CHANNEL='mock_channel'
        ).send('msg')
        self.assertTrue(not result['ok'])


    @tag('slackreminder_create_options')
    @patch('requests.post')
    def tests_slackreminder_create_options(self, request_mock):
        # python manage.py test --tag=slackreminder_create_options
        options = [
            'Corn pie and Dessert',
            'Chicken Nugget Rice',
        ]
        menu_id = '00000000-0000-0000-0000-000000000001'
        request_mock.return_value = RequestMock(mode='success')
        result = SlackReminder().create_options(options)
        self.assertListEqual(
            result,
            [
                'Option 1: Corn pie and Dessert',
                'Option 2: Chicken Nugget Rice'
            ]
        )
        
        '''
        > Option 1: Corn pie, Salad and Dessert
> Option 2: Chicken Nugget Rice, Salad and Dessert
> Option 3: Rice with hamburger, Salad and Dessert
> Option 4: Premium chicken Salad and Dessert.
        '''

    @tag('slackreminder_construct_msg')
    @patch('requests.post')
    def tests_slackreminder_construct_msg(self, request_mock):
        # python manage.py test --tag=slackreminder_construct_msg
        options = [
            'Corn pie and Dessert',
            'Chicken Nugget Rice',
        ]
        menu_id = '00000000-0000-0000-0000-000000000001'
        request_mock.return_value = RequestMock(mode='success')
        result = SlackReminder().construct_msg(options, menu_id)
        self.assertEqual(
            result,
            'Hello!\nI share with you today\'s menu :)\n\n<http://localhost:8000/menu/00000000-0000-0000-0000-000000000001>\n\nCorn pie and Dessert\nChicken Nugget Rice\nHave a nice day!'
        )

    @tag('slackreminder_send_success')
    @patch('requests.post')
    def tests_slackreminder_send_success(self, request_mock):
        # python manage.py test --tag=slackreminder_send_success
        options = [
            'Corn pie and Dessert',
            'Chicken Nugget Rice',
        ]
        menu_id = '00000000-0000-0000-0000-000000000001'
        request_mock.return_value = RequestMock(mode='success')
        result = SlackReminder().send(options, menu_id)
        self.assertTrue(result['ok'])


@tag('scheduler')
@override_settings(
)
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
        #menu = Menu.objects.last()
        
        print(meals)
        #for m in meals:
        #    menu.meals.add(m)
        for mm in menu.meals.all():
            print(mm)

        # schedule_menu_process(menu)
    
    