# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Standard libs
from .exceptions import ExistingUserEmailException
from django.contrib.auth.models import User


def exist_email_user(email):
    try:
        User.objects.get(email=email.lower())
    except User.DoesNotExist:
        return False
    else:
        return True


def create_user(data):
    if not exist_email_user(data.get('email')):
        user = User.objects.create_user(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            username=data.get('email').lower(),
            email=data.get('email').lower(),
            password=data.get('password')
        )
        return user
    else:
        raise ExistingUserEmailException()
