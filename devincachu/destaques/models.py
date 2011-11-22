# -*- coding: utf-8 -*-
import roan

from django.contrib.auth import models as auth_models
from django.db import models


class Destaque(models.Model):
    titulo = models.CharField(max_length=60)
    conteudo = models.CharField(max_length=500)
    autor = models.ForeignKey(auth_models.User)
    data = models.DateTimeField(auto_now=False, auto_now_add=True)


class Chamada(Destaque):
    titulo_veja_mais = models.CharField(max_length=40)
    url_link = models.URLField(verify_exists=False, max_length=255)

roan.purge("/").on_save(Destaque)
roan.purge("/").on_delete(Destaque)
roan.purge("/").on_save(Chamada)
roan.purge("/").on_delete(Chamada)
