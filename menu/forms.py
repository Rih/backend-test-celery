# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Standard libs
from django import forms
from dashboard.models import Meal
from menu.models import Order
from menu.bl.data import FORMS_PLACEHOLDER


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('meal', 'name', 'email', 'suggestion')

    placeholder = FORMS_PLACEHOLDER['order']
    meal = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-4',
                'placeholder': placeholder['meal'],
                'required': True,
            }
        )
    )
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-4',
                'placeholder': placeholder['name'],
                'required': True,
            }
        )
    )
    email = forms.EmailField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control  mb-4',
                'type': 'email',
                'placeholder': placeholder['email'],
                'required': True,
            }
        )
    )
    suggestion = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control ',
                'placeholder': placeholder['suggestion'],
                'rows': 3,
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['meal'] = Meal.objects.get(pk=cleaned_data.get('meal'))
        return cleaned_data
