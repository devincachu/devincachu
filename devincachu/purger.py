# -*- coding: utf-8 -*-
import roan

from django.contrib.flatpages import models


def connect():
    flatpages = models.FlatPage.objects.all()
    for f in flatpages:
        roan.purge(f.url).on_save(models.FlatPage)
