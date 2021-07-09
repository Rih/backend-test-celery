# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Standard libs
# Django libs
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
# Own libs
from dashboard.models import Menu
from menu.forms import OrderForm
from menu.bl.utils import (
    handle_menu_date,
    handle_current_date,
)
from menu.exceptions import InvalidMenuException


# Create your views here.


class MenuView(FormView):
    template_name = 'menu/index.html'
    form_class = OrderForm
    success_url = reverse_lazy('menu:menu_done')

    def get_initial(self):
        return {
            'name': self.request.session.get('name'),
            'email': self.request.session.get('email'),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = Menu.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        self.request.session['name'] = form.cleaned_data['name']
        self.request.session['email'] = form.cleaned_data['email']
        try:
            valid_menu = handle_menu_date(self.kwargs['pk'])
            valid_date = handle_current_date()
            if form.is_valid() and valid_date and valid_menu:
                form.save()
        except InvalidMenuException as e:
            form.add_error(None, e.error_msg())
            return super().form_invalid(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


public_menu_view = MenuView.as_view()
