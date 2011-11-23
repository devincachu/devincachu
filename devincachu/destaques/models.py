# -*- coding: utf-8 -*-
import roan

from django.contrib.auth import models as auth_models
from django.db import models


class Destaque(models.Model):
    titulo = models.CharField(max_length=60)
    conteudo = models.CharField(max_length=500)
    autor = models.ForeignKey(auth_models.User)
    data = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __repr__(self):
        return "<Destaque: %s>" % self.titulo

    def __unicode__(self):
        return self.titulo


class Chamada(Destaque):
    titulo_veja_mais = models.CharField(max_length=40)
    url_link = models.CharField(max_length=255)

    def __repr__(self):
        return "<Chamada: %s>" % self.titulo

roan.purge("/").on_save(Destaque)
roan.purge("/").on_delete(Destaque)
roan.purge("/").on_save(Chamada)
roan.purge("/").on_delete(Chamada)
