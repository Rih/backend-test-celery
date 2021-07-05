# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView
from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('/meals', views.meal_list_view, name='meals'),
    path('/meals/create/<int:pk>/', views.meal_partial_view, name='meals_create'),
    path('/meals/edit/<int:pk>/', views.meal_partial_view, name='meals_edit'),
    #path('/meal/<int:pk>', views.meal_view, name='meal'),
    path('/menus', views.menu_list_view, name='menus'),
    path('/orders', views.order_view, name='orders'),

]
