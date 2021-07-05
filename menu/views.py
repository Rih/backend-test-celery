# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Standard libs
# Django libs
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
# Own libs
from dashboard.models import Meal, Menu
from menu.forms import OrderForm

# Create your views here.


class MenuView(FormView):
    template_name = 'menu/index.html'
    form_class = OrderForm
    success_url = reverse_lazy('menu:menu_done')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu = Menu.objects.get(pk=self.kwargs.get('pk'))
        context['menu'] = menu
        context['meals'] = enumerate(menu.meals.all())
        return context
    
    def form_valid(self, form):
        # form.save()
        self.request.session['name'] = form.cleaned_data['name']
        self.request.session['email'] = form.cleaned_data['email']
        if form.is_valid():
            form.save()
        return super().form_valid(form)

    
public_menu_view = MenuView.as_view()

