# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from django.db import models
from dashboard.managers import MealManager, MenuManager
from django.utils import timezone
# Create your models here.


class Meal(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    objects = MealManager()
    modified_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(null=True)
    
    def __str__(self):
        return f'{self.id}:  {self.title}'
    
    def delete(self):
        if self.deleted_at:
            return
        self.deleted_at = timezone.now()
        self.save()
    

class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meals = models.ManyToManyField(Meal)
    objects = MenuManager()
    scheduled_at = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)

    def delete(self):
        # TODO: implement pre_delete to unlink a current task
        if self.deleted_at:
            return
        self.deleted_at = timezone.now()
        self.save()


class TaskMenu(models.Model):
    celery_task_id = models.CharField(max_length=200, blank=True, default='')
    celery_status = models.IntegerField(default=0)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    

