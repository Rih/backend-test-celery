# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Standard libs
from django import forms
from captcha.fields import ReCaptchaField


class SignupForm(forms.Form):

    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control ',
                'placeholder': 'Nombre'
            }
        )
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control ',
                'placeholder': 'Apellido'
            }
        )
    )

    email = forms.EmailField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control ',
                'placeholder': 'Email'
            }
        )
    )
    password = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control ',
                'placeholder': 'Contraseña',
                'type': 'password',
                'autocomplete': 'off'
            }
        )
    )
    captcha = ReCaptchaField()


class LoginForm(forms.Form):

    email = forms.EmailField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control ',
                'placeholder': 'Email'
            }
        )
    )
    password = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control ',
                'placeholder': 'Contraseña',
                'type': 'password',
                'autocomplete': 'off'
            }
        )
    )
    captcha = ReCaptchaField()
