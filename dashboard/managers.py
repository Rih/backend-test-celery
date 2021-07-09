# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class BaseQuerySet(models.QuerySet):
    pass


class BaseManager(models.Manager):

    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db)

    def actives(self, user):
        qset = self.get_queryset()
        return qset.filter(deleted_at=None, author_id=user.id)

    def latest_first(self, user):
        qset = self.actives().filter(author_id=user.id)
        return qset.order_by('-scheduled_at')

    def all(self):
        return self.get_queryset()


class MealManager(BaseManager):
    pass


class MenuManager(BaseManager):
    pass
