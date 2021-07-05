# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Standard libs
import uuid, json
# Django libs
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic import  ListView
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from django.conf import settings
# Own libs
from dashboard.serializers import MealModelSerializer
from dashboard.models import Meal, Menu
from menu.models import Order
# Create your views here.


class MealListView(ListView):
    template_name = 'dashboard/meal_list.html'
    model = Meal
    queryset = Meal.objects.actives()
    fields = ['title']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = enumerate(context['object_list'])
        context['form_id'] = 'meal_form'
        context['form_id_edit'] = 'meal_form_edit'
        context['modal_id'] = 'meal_modal'
        context['modal_id_edit'] = 'meal_edit_modal'
        return context


meal_list_view = login_required(MealListView.as_view())


class MenuListView(ListView):
    template_name = 'dashboard/menu_list.html'
    model = Menu
    queryset = Menu.objects.actives()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = enumerate(context['object_list'])
        context['form_id'] = 'menu_form'
        context['form_id_edit'] = 'menu_form_edit'
        context['modal_id'] = 'menu_modal'
        context['modal_title'] = 'New Menu'
        return context


menu_list_view = login_required(MenuListView.as_view())


class IndexView(ListView):
    template_name = 'dashboard/index.html'
    model = Meal
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meals'] = Meal.objects.count()
        context['menus'] = Menu.objects.count()
        context['orders'] = Order.objects.count()
        context['latest_menu'] = Menu.objects.last()
        return context


index_view = login_required(IndexView.as_view())


class OrderView(ListView):
    template_name = 'dashboard/order_list.html'
    model = Order
    queryset = Order.objects.all().order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


order_view = login_required(OrderView.as_view())


class PartialView(TemplateView):
    template_name = 'base-modal.html'
    model = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = None
        if self.model and kwargs.get('pk'):
            object = self.model.objects.get(pk=kwargs['pk'])
        model_name = self.request.GET.get('model')
        title = self.request.GET.get('title')
        context['form_id'] = f'{model_name}_form'
        context['modal_id'] = f'{model_name}_modal'
        context['modal_title'] = title
        context['object'] = object
        return context


class MealPartialView(PartialView):
    template_name = 'partials/_modal_meal.html'
    model = Meal
    

meal_partial_view = login_required(MealPartialView.as_view())

