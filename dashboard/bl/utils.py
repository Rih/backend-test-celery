# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Standard libs
import logging
from datetime import datetime as dt, timedelta
from django.conf import settings
from dashboard.models import Menu
from dashboard.bl.data import FAKE_MENU_IDS


logger = logging.getLogger(__name__)


def on_msg(body):
    print(body)


def get_current_date() -> dt:
    today = dt.utcnow()
    return today


def get_near_future_task(scheduled: dt) -> dt:
    today = get_current_date()
    schedule_time = settings.SCHEDULE_MENU_TIME
    delta = timedelta(**schedule_time)
    near_future = dt.combine(
        scheduled,
        (dt.min + delta).time()
    )
    if scheduled <= today.date():
        near_future = today + timedelta(minutes=5)
    return near_future


def omit_menues(instance: Menu) -> bool:
    return str(instance.pk.urn[9:]) in FAKE_MENU_IDS
