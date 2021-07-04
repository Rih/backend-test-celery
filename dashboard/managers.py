# -*- coding: utf-8 -*-
import uuid
from django.db import models


class BaseQuerySet(models.QuerySet):
    pass


class BaseManager(models.Manager):
    
    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db)
    
    def actives(self):
        qset = self.get_queryset()
        return qset.filter(deleted_at=None)
    
    def all(self):
        return self.get_queryset()
    

class MealManager(BaseManager):
    pass


class MenuManager(BaseManager):
    pass

    # def create(self, *args, **kwargs):
    #     return super().create(*args, **kwargs)