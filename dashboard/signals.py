# Standard libs
import logging
from datetime import datetime, timedelta
from django.conf import settings
from dashboard.models import Menu, TaskMenu
from django.db.models.signals import post_save, pre_save
from celery import chain
from django.dispatch import receiver
from backend_test.tasks import schedule_menu_process


logger = logging.getLogger(__name__)


def on_msg(body):
    print(body)


# method for schedule async after menu is created
@receiver(post_save, sender=Menu, dispatch_uid="schedule_menu_signal")
def schedule_menu(sender, instance, created, **kwargs):
    if created:
        tomorrow = datetime.utcnow() + timedelta(hours=-4)
        # task = schedule_menu_process.apply_async(args=[instance.pk], eta=10)
        task = schedule_menu_process.apply_async(args=[instance.pk], countdown=10)
        import pdb; pdb.set_trace()
        #task = schedule_menu_process.s(instance.pk)
        #print(task.get(on_message=on_msg, propagate=False))
        task_menu = TaskMenu.objects.create(
            menu=instance,
            celery_task_id=task
        )
        # task.apply_async(eta=tomorrow)
