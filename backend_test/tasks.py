import logging
import os
from celery import Task
from celery.contrib import rdb
from django.conf import settings
from dashboard.models import Menu
from dashboard.bot import SlackReminder
from backend_test.celery import app

logger = logging.getLogger(__name__)


class MenuTask(Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        menu = Menu.objects.get(pk=args[0])
        # menu.save()
        logger.error('Task {0} raised exception: {1!r}\n{2!r}'.format(task_id, exc, einfo))


@app.task(base=MenuTask)
def schedule_menu_process(menu_id):
    menu = Menu.objects.get(pk=menu_id)
    meals = [m.title for m in menu.meals.all()]
    result = SlackReminder().send(meals, menu.pk)
    return {
        'result': result,
    }
