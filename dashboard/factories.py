# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import factory
from dashboard.models import Meal, Menu


class MenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Menu


class MealFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Meal

    title = 'Chicken with potatoe chips'
