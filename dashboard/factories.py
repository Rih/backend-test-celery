# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import factory
from datetime import datetime as dt
from dashboard.models import Meal, Menu


class MealFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Meal

    title = 'Chicken with potatoe chips'


class MenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Menu
    scheduled_at = dt.utcnow().date()
    meals = factory.SubFactory(Meal)

    @factory.post_generation
    def meals(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for meal in extracted:
                self.meals.add(meal)
