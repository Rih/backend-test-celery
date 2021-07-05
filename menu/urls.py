# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Django libs
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView
from menu import views

app_name = 'menu'

urlpatterns = [
    path('menu/<str:pk>', views.public_menu_view, name='menu_list'),
    path(
        'menu-done',
        TemplateView.as_view(
            template_name='menu/done.html'
        ),
        name='menu_done'
    ),

]
