# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Standard libs
from datetime import datetime, timedelta
# Django libs
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
# Own libs
from dashboard.models import Meal, Menu
from dashboard.data import MODEL_TO_MODAL_NAMES
from menu.models import Order
# Create your views here.


class MealListView(TemplateView):
    template_name = 'dashboard/meal_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['partial_names'] = MODEL_TO_MODAL_NAMES['meal']
        return context


meal_list_view = login_required(MealListView.as_view())


class MenuListView(ListView):
    template_name = 'dashboard/menu_list.html'
    model = Menu
    queryset = Menu.objects.latest_first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = enumerate(context['object_list'])
        context['partial_names'] = MODEL_TO_MODAL_NAMES['menu']
        return context


menu_list_view = login_required(MenuListView.as_view())


class IndexView(TemplateView):
    template_name = 'dashboard/index.html'

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
        mode = self.request.GET.get('mode')  # edit or create
        context.update(MODEL_TO_MODAL_NAMES[model_name][mode])
        context['object'] = object
        return context


class MealPartialView(PartialView):
    template_name = 'partials/_modal_meal.html'
    model = Meal


meal_partial_view = login_required(MealPartialView.as_view())


class MenuPartialView(PartialView):
    template_name = 'partials/_modal_menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meals'] = Meal.objects.actives()
        tomorrow = datetime.utcnow() + timedelta(hours=-4)
        context['tomorrow'] = tomorrow.strftime('%Y-%m-%d')
        return context


menu_partial_view = login_required(MenuPartialView.as_view())
