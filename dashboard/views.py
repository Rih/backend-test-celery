# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Standard libs
import uuid, json
# Django libs
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from django.conf import settings
# Own libs
from dashboard.serializers import MealModelSerializer
from dashboard.models import Meal, Menu
from dashboard.forms import MealForm
# Create your views here.


class MealListView(ListView):
    template_name = 'dashboard/meal_list.html'
    model = Meal
    form_class = MealForm
    fields = ['title']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


meal_list_view = login_required(MealListView.as_view())


class MenuView(CreateView):
    template_name = 'dashboard/menu_create.html'
    model = Menu
    
    def post(self, request, **kwargs):
        menu = Menu.objects.create(
            pk=str(uuid.uuid4()),
        )
    

menu_view = login_required(MenuView.as_view())


class IndexView(ListView):
    template_name = 'dashboard/index.html'
    model = Meal
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error'] = 'nooo'
        return context


index_view = login_required(IndexView.as_view())


class OrderView(DetailView):
    template_name = 'dashboard/index.html'
    model = Meal
    
    def get_object(self):
        return self.get_object_or_404(
            pk=self.kwargs['pk']
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error'] = 'nooo'
        return context
