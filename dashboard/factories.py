import factory
from dashboard.models import Meal, Menu
from django.contrib.auth.models import User


class MenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Menu


class MealFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Meal

    title = 'Pollos con papas'