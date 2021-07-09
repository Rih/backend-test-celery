# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Django libs
from django.urls import path
from django.views.generic import TemplateView
from menu import views

app_name = 'menu'

urlpatterns = [
    path(
        '',
        TemplateView.as_view(
            template_name='landing.html'
        ),
        name='index'
    ),
    path('menu/<str:pk>', views.public_menu_view, name='menu_list'),
    path(
        'order/done',
        TemplateView.as_view(
            template_name='menu/done.html'
        ),
        name='menu_done'
    ),

]
