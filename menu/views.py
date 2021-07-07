# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Standard libs
from datetime import datetime as dt
# Django libs
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
# Own libs
from dashboard.models import Menu
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
        self.request.session['name'] = form.cleaned_data['name']
        self.request.session['email'] = form.cleaned_data['email']
        menu = Menu.objects.get(pk=self.kwargs['pk'])
        today = dt.utcnow()
        if today.date() > menu.scheduled_at:  # TODO: add test
            form.add_error('scheduled_at', 'Menu is from the past, are you a time traveler?')
            return super().form_invalid(form)
        if today.hour >= settings.MAX_HOUR_TO_ORDER:  # TODO: add test
            form.add_error('scheduled_at', 'Not a valid time')
            return super().form_invalid(form)
        if form.is_valid():
            form.save()
        return super().form_valid(form)


public_menu_view = MenuView.as_view()
