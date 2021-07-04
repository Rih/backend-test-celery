# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Standard libs
import factory
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .models import EmailToken


@factory.django.mute_signals(post_save)
class EmailTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmailToken

    token = factory.Faker('pystr_format')
    user = factory.SubFactory(
        'account.factories.UserFactory', email_token=None)


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = 'John'
    last_name = 'Doe'
    username = factory.Sequence(lambda n: 'username %d' % n)

    email_token = factory.RelatedFactory(
        EmailTokenFactory, factory_related_name='user')
