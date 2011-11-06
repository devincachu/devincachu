# -*- coding: utf-8 -*-

from django.contrib.auth import models as auth_models
from django.db import models


class Destaque(models.Model):
    titulo = models.CharField(max_length=60)
    conteudo = models.CharField(max_length=500)
    autor = models.ForeignKey(auth_models.User)
    data = models.DateTimeField(auto_now=False, auto_now_add=True)
