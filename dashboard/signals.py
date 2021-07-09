# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Standard libs
import logging
from dashboard.models import Menu, TaskMenu
from django.db.models.signals import post_save
# from celery import chain
# from celery.contrib import rdb
from dashboard.bl.utils import (
    # on_msg,
    get_near_future_task,
    omit_menues,
)
from django.dispatch import receiver
from backend_test.tasks import schedule_menu_process


logger = logging.getLogger(__name__)


# method for schedule async after menu is created
@receiver(post_save, sender=Menu, dispatch_uid="schedule_menu_signal")
def schedule_menu(sender, instance, created, **kwargs):
    if created:
        # omit menus for tests
        scheduled = instance.scheduled_at
        if omit_menues(instance) or not scheduled:
            logger.info('Not sending scheduled menu')
            return
        near_future = get_near_future_task(scheduled)
        task = schedule_menu_process.apply_async(
            args=[instance.pk],
            eta=near_future,
            retry=False,
        )
        TaskMenu.objects.create(
            menu=instance,
            celery_task_id=task
        )
        return near_future
