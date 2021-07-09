# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Standard libs
from django import forms
from captcha.fields import ReCaptchaField
# Own libs
from account.bl.data import FORMS_PLACEHOLDER


class SignupForm(forms.Form):
    placeholder = FORMS_PLACEHOLDER['signup']
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control ',
                'placeholder': placeholder['first_name']
            }
        )
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control ',
                'placeholder': placeholder['last_name']
            }
        )
    )
    email = forms.EmailField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control ',
                'placeholder': placeholder['email']
            }
        )
    )
    password = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control ',
                'placeholder': placeholder['password'],
                'type': 'password',
                'autocomplete': 'off'
            }
        )
    )
    captcha = ReCaptchaField()


class LoginForm(forms.Form):

    placeholder = FORMS_PLACEHOLDER['login']
    email = forms.EmailField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control ',
                'placeholder': placeholder['email']
            }
        )
    )
    password = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control ',
                'placeholder': placeholder['password'],
                'type': 'password',
                'autocomplete': 'off'
            }
        )
    )
    captcha = ReCaptchaField()
