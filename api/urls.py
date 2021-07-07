# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from api import views
from rest_framework import routers
router = routers.SimpleRouter()
router.register(r'/meals', views.MealViewSet, basename='meals_action')
router.register(r'/menu-list', views.MenuReadViewSet, basename='menulist_action')
router.register(r'/menus', views.MenuViewSet, basename='menus_action')

app_name = 'api'

urlpatterns = router.urls
