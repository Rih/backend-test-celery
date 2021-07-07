# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Standard libs
# Django libs
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
# Own libs
from dashboard.serializers import (
    MealModelSerializer,
    MenuModelSerializer,
    MenuModelListSerializer,
)
from dashboard.models import Meal, Menu
# Create your views here.


class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealModelSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = Meal.objects.actives()


class MenuReadViewSet(viewsets.ModelViewSet):
    serializer_class = MenuModelListSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = Menu.objects.actives()


class MenuViewListSet(viewsets.ModelViewSet):
    serializer_class = MenuModelListSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = Menu.objects.latest_first()


class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuModelSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = Menu.objects.actives()
