# -*- coding: utf-8 -*-
from django.db import models


class Palestrante(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    minicurriculo = models.CharField(max_length=1000)
    blog = models.URLField(verify_exists=False, max_length=255, blank=True)
    twitter = models.CharField(max_length=50, blank=True)
    foto = models.ImageField(upload_to=u"palestrantes")

    def __repr__(self):
        return '<Palestrante: "%s">' % self.nome

    def __unicode__(self):
        return self.nome


class Palestra(models.Model):
    titulo = models.CharField(max_length=150, verbose_name=u"Título")
    slug = models.SlugField(max_length=150, unique=True)
    descricao = models.CharField(max_length=1000, verbose_name=u"Descrição")
    inicio = models.TimeField(verbose_name=u"Horário de início")
    termino = models.TimeField(verbose_name=u"Horário de término")
    palestrantes = models.ManyToManyField(Palestrante, blank=True)

    def nomes_palestrantes(self):
        nomes = [p.nome for p in self.palestrantes.order_by("nome")]
        nomes = ", ".join(nomes)

        if "," in nomes:
            indice = nomes.rfind(",")
            nomes = "%s e %s" % (nomes[:indice], nomes[indice + 2:])

        return nomes
