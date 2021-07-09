# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from menu.bl.data import ERROR_MESSAGES


class InvalidMenuException(Exception):
    error_code = None

    def __init__(self, error_code):
        Exception.__init__(self)
        self.error_code = error_code

    def error_msg(self):
        if self.error_code:
            return ERROR_MESSAGES[self.error_code]
        return ''
