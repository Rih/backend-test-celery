# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
# # Standard libs
from datetime import datetime as dt, timedelta
# # Django libs
from django.test import TestCase, tag, override_settings
from unittest.mock import patch
# # Own libs
from menu.exceptions import InvalidMenuException
from menu.bl.utils import handle_menu_date, handle_current_date
from dashboard.factories import MenuFactory


@tag('menu_utils')
class UtilsTest(TestCase):

    @tag('handle_menu_date')
    def tests_utils_handle_menu_date(self):
        # python manage.py test --tag=handle_menu_date
        yesterday = dt.now() + timedelta(days=-1)
        fail_menu = MenuFactory(
            scheduled_at=yesterday.date()
        )
        with self.assertRaises(InvalidMenuException):
            handle_menu_date(fail_menu.pk)
        mock_time = dt.combine(
            dt.now().date(),
            (dt.min + timedelta(days=1)).time()
        )
        new_menu = MenuFactory(
            scheduled_at=mock_time.date()
        )
        result = handle_menu_date(new_menu.pk)
        self.assertTrue(result)

    @tag('handle_current_date_invalid')
    @override_settings(
        MAX_HOUR_TO_ORDER=1,
        UTC_TZ_OFFSET=0,
    )
    @patch('dashboard.bl.utils.get_current_date')
    def tests_utils_handle_current_date_invalid(self, nowmock):
        # python manage.py test --tag=handle_current_date_invalid
        mock_time = dt.combine(
            dt.now().date(),
            (dt.min + timedelta(hours=9)).time()
        )
        nowmock.return_value = mock_time
        with self.assertRaises(InvalidMenuException):
            handle_current_date()

    @tag('handle_current_date_success')
    @override_settings(
        MAX_HOUR_TO_ORDER=23,
        UTC_TZ_OFFSET=0,
    )
    @patch('dashboard.bl.utils.get_current_date')
    def tests_utils_handle_current_date_success(self, nowmock):
        # python manage.py test --tag=handle_current_date_success
        mock_time = dt.combine(
            dt.now(),
            (dt.min + timedelta(hours=1)).time()
        )
        nowmock.return_value = mock_time
        result = handle_current_date()
        self.assertTrue(result)
