# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Standard libs
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.urls import reverse_lazy
from django.template.loader import render_to_string
import datetime


class EmailToken(models.Model):

    token = models.CharField(max_length=30, blank=True, default='')
    verified = models.BooleanField(default=False)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    last_email_sent = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_email_confirmation_url(self):
        current_site = Site.objects.get_current()
        return 'http://' + str(current_site.domain) + \
            str(
                reverse_lazy(
                    'account:verify_email', kwargs={'token': self.token}))

    def send_confirmation_email(self):
        html_email = 'account/emails/email_registration.html'
        plain_email = 'account/emails/email_registration.txt'
        msg_plain = render_to_string(
            plain_email,
            {'user': self.user}
        )
        msg_html = render_to_string(
            html_email,
            {'user': self.user}
        )
        self.user.email_user(
            'Welcome!',
            msg_plain,
            html_message=msg_html
        )
        self.last_email_sent = datetime.datetime.now(
            datetime.timezone.utc
        )
        self.save()
