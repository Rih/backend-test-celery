# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.sites.models import Site


def append_global_vars(request):
    current_site = Site.objects.get_current()
    return {
        'base_url': current_site.domain,
    }
