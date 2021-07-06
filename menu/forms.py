# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Standard libs
from django import forms
from dashboard.models import Meal
from menu.models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('meal', 'name', 'email', 'suggestion')

    meal = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-4',
                'placeholder': 'Your Meal',
                'required': True,
            }
        )
    )

    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-4',
                'placeholder': 'Your Name',
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
                'placeholder': 'Your Email',
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
                'placeholder': 'Additional info (ex: No ketchup and more rice)',
                'rows': 3,
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['meal'] = Meal.objects.get(pk=cleaned_data.get('meal'))
        return cleaned_data
