# -*- coding: utf-8 -*-

from django.conf import settings


def get_base_url(request):
    return {u"BASE_URL": settings.BASE_URL}
