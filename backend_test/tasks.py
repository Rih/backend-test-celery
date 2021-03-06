# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from celery import Task
# from celery.contrib import rdb
from dashboard.models import Menu
from dashboard.bl.bot import SlackReminder
from backend_test.celery import app

logger = logging.getLogger(__name__)


class MenuTask(Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # menu = Menu.objects.get(pk=args[0])
        # menu.save()
        # import pdb; pdb.set_trace()
        logger.error(
            'Task {0} raised exception: {1!r}\n{2!r}'.format(
                task_id, exc, einfo
            )
        )


@app.task(base=MenuTask)
def schedule_menu_process(menu_id):
    # menu_id = kwargs.get('menu_id')
    menu = Menu.objects.get(pk=menu_id)
    meals = [m.title for m in menu.meals.all()]
    result = SlackReminder().send(meals, menu.pk)
    return {
        'result': result,
    }

# celery -A backend_test worker -l INFO
