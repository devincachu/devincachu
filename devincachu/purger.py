# -*- coding: utf-8 -*-
import roan

from django.contrib.flatpages import models

from palestras import models as pmodels


def connect():
    flatpages = models.FlatPage.objects.all()
    for f in flatpages:
        roan.purge(f.url).on_save(models.FlatPage)

    palestras = pmodels.Palestra.objects.all()
    for p in palestras:
        roan.purge(p.get_absolute_url_and_link_title()['url']).on_save(pmodels.Palestra)
        roan.purge(p.get_absolute_url_and_link_title()['url']).on_delete(pmodels.Palestra)
