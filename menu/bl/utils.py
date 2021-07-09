# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Standard libs
# Django libs
from django.conf import settings
from dashboard.models import Menu
from dashboard.bl.utils import get_current_date
from menu.exceptions import InvalidMenuException


def handle_menu_date(pk: str) -> bool:
    menu = Menu.objects.get(pk=pk)
    today = get_current_date()
    invalid = today.date() > menu.scheduled_at
    if invalid:
        raise InvalidMenuException('invalid_menu')
    return True


def handle_current_date() -> bool:
    today = get_current_date()
    if today.hour + settings.UTC_TZ_OFFSET >= settings.MAX_HOUR_TO_ORDER:
        raise InvalidMenuException('invalid_date')
    return True
