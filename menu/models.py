# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Standard libs
from django.db import models
from dashboard.models import Meal

# Create your models here.


class Order(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.PROTECT)
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=50)
    suggestion = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
