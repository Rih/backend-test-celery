# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Standard libs
import uuid, json
# Django libs
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
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


class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuModelSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = Menu.objects.actives()

#    def create(self, request, **kwargs):
#        import pdb; pdb.set_trace()
