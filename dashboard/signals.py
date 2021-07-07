# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Standard libs
import logging
from datetime import datetime as dt, timedelta
from dashboard.models import Menu, TaskMenu
from django.db.models.signals import post_save
from django.conf import settings
# from celery import chain
# from celery.contrib import rdb
from dashboard.data import FAKE_MENU_IDS
from django.dispatch import receiver
from backend_test.tasks import schedule_menu_process


logger = logging.getLogger(__name__)


def on_msg(body):
    print(body)


# method for schedule async after menu is created
@receiver(post_save, sender=Menu, dispatch_uid="schedule_menu_signal")
def schedule_menu(sender, instance, created, **kwargs):
    if created:
        # omit menus for tests
        if str(instance.pk.urn[9:]) not in FAKE_MENU_IDS:
            scheduled = instance.scheduled_at
            today = dt.utcnow()
            schedule_time = settings.SCHEDULE_MENU_TIME
            delta = timedelta(**schedule_time)
            near_future = dt.combine(
                scheduled,
                (dt.min + delta).time()
            )
            if scheduled <= today.date():
                near_future = today + timedelta(minutes=5)
            task = schedule_menu_process.apply_async(
                args=[instance.pk],
                eta=near_future,
                retry=False,
            )
            # task = schedule_menu_process.apply_async(menu_id=instance.pk, countdown=10)
            # print(task.get(on_message=on_msg, propagate=False))
            TaskMenu.objects.create(
                menu=instance,
                celery_task_id=task
            )
            return near_future
        else:
            print('Not sending scheduled menu')
            # task()
            # task.apply_async(eta=tomorrow)
