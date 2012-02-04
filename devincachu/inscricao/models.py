# -*- coding: utf-8 -*-
import roan

from django.db import models


class Participante(models.Model):
    TAMANHOS_DE_CAMISETA = (
        (u'P', u'P'),
        (u'M', u'M'),
        (u'G', u'G'),
        (u'GG', u'GG'),
    )

    SEXOS = (
        (u'M', u'Masculino'),
        (u'F', u'Feminino'),
    )

    nome = models.CharField(max_length=100)
    nome_cracha = models.CharField(max_length=100, blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=SEXOS)
    email = models.EmailField(max_length=100)
    confirmado = models.BooleanField(default=False)
    tamanho_camiseta = models.CharField(max_length=2, verbose_name=u"Tamanho da camiseta", choices=TAMANHOS_DE_CAMISETA)
    instituicao_ensino = models.CharField(max_length=100, verbose_name=u"Instituição de ensino (para estudantes)", blank=True, null=True)
    empresa = models.CharField(max_length=100, verbose_name=u"Empresa onde trabalha", blank=True, null=True)

    def __unicode__(self):
        return self.nome


class Configuracao(models.Model):
    STATUS = (
        (u"fechadas", u"Fechadas (inscrições ainda não abriram)"),
        (u"abertas", u"Inscrições abertas"),
        (u"encerradas", u"Inscrições encerradas"),
    )

    valor_inscricao = models.FloatField(verbose_name=u"Valor da inscrição")
    status = models.CharField(max_length=10, choices=STATUS)

    def __unicode__(self):
        return u"Configuração das inscrições do Dev in Cachu 2012"

    class Meta:
        verbose_name = u"Configuração das inscrições"
        verbose_name_plural = verbose_name

roan.purge("/inscricao/").on_save(Configuracao)
