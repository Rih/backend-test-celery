# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
import json
import logging
from django.conf import settings
from django.contrib.sites.models import Site

log = logging.getLogger(__name__)


class SlackBot:

    TOKEN = settings.SLACK_OAUTH_TOKEN

    def __init__(self, **kwargs):
        self.CHANNEL = kwargs.get('CHANNEL', settings.SLACK_CHANNEL_ID)
        self.BASE_URL = 'https://api.slack.com'
        self.h = {
            'Authorization': f'Bearer {self.TOKEN}',
            'Content-Type': 'application/json',
        }

    def send(self, text: str):
        endpoint = '/api/chat.postMessage'
        payload = {
            'channel': self.CHANNEL,
            'text': text
        }
        response = requests.post(
            f'{self.BASE_URL}{endpoint}',
            headers=self.h,
            data=json.dumps(payload)
        )
        result = response.json()
        return result


class SlackReminder:

    msg_greetings = [
        'Hello!',
        'I share with you today\'s menu :)',
        '',
    ]
    msg_farewell = [
        '',
        'Have a nice day!',
    ]

    def __init__(self):
        self.bot = SlackBot()

    def create_options(self, options) -> list:
        opts = [
            f'Option {i + 1}: {opt}' for i, opt in enumerate(options)
        ]
        return opts

    def construct_msg(self, opts: list, menu_id: str) -> str:
        text = '\n'.join(self.msg_greetings)
        current_site = Site.objects.get_current()
        domain = current_site.domain
        text += f'\n<{domain}/menu/{menu_id}>\n\n'
        text += '\n'.join(opts)
        text += '\n'.join(self.msg_farewell)
        return text

    def send(self, menu_options: list, menu_id: str) -> dict:
        text = self.construct_msg(self.create_options(menu_options), menu_id)
        result = self.bot.send(text)
        return result


if __name__ == '__main__':
    pass
