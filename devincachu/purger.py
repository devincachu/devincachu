# -*- coding: utf-8 -*-
import roan

from django.contrib.flatpages import models

flatpage_urls = ("/caravanas/", "/contato/", "/quando-e-onde/", "/inscricao/", "/patrocinio/")


def connect():
    for url in flatpage_urls:
        roan.purge(url).on_save(models.FlatPage)
