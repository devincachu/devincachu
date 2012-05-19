# -*- coding: utf-8 -*-
import roan

from django.db import models


class Participante(models.Model):
    TAMANHOS_DE_CAMISETA = (
        (u'P', u'P (53cm x 71cm)'),
        (u'M', u'M (56cm x 74cm)'),
        (u'G', u'G (58cm x 76cm)'),
        (u'GG', u'GG (62cm x 80cm)'),
    )

    SEXOS = (
        (u'M', u'Masculino'),
        (u'F', u'Feminino'),
    )

    STATUS = (
        (u'AGUARDANDO', u'Aguardando pagamento'),
        (u'CONFIRMADO', u'Confirmado'),
        (u'CANCELADO', u'Cancelado'),
        (u'CORTESIA', u'Cortesia'),
        (u'PALESTRANTE', u'Palestrante'),
        (u'ORGANIZACAO', u'Organização'),
        (u'CARAVANA', u'Caravana'),
    )

    nome = models.CharField(max_length=100)
    nome_cracha = models.CharField(max_length=100, verbose_name=u"Nome no crachá", blank=True, null=True)
    cidade = models.CharField(max_length=255, verbose_name=u"Cidade/Estado")
    sexo = models.CharField(max_length=1, choices=SEXOS)
    email = models.EmailField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS, default=u'AGUARDANDO')
    tamanho_camiseta = models.CharField(max_length=2, verbose_name=u"Tamanho da camiseta", choices=TAMANHOS_DE_CAMISETA)
    instituicao_ensino = models.CharField(max_length=100, verbose_name=u"Instituição de ensino (para estudantes)", blank=True, null=True)
    empresa = models.CharField(max_length=100, verbose_name=u"Empresa onde trabalha", blank=True, null=True)

    def __unicode__(self):
        return self.nome

    class Meta:
        unique_together = ((u'email', u'status',),)


class Checkout(models.Model):
    codigo = models.CharField(max_length=100)
    participante = models.ForeignKey(Participante)

    def __unicode__(self):
        return "%s (%s - %s)" % (self.codigo, self.participante.nome, self.participante.email)


class Certificado(models.Model):
    participante = models.ForeignKey(Participante)
    codigo = models.CharField(max_length=14)
    hash = models.CharField(max_length=100)
    horas = models.IntegerField(default=8)

    def __unicode__(self):
        return "%s (%s)" % (self.codigo, self.participante.nome)


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
