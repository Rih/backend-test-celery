from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView
from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('/meals', views.meal_list_view, name='meals'),
    #path('/meal/<int:pk>', views.meal_view, name='meal'),
    path('/menus', views.menu_view, name='menus'),
    path('/menu/<str:pk>', views.menu_view, name='menu'),
    path('/orders', views.menu_view, name='orders'),

]
