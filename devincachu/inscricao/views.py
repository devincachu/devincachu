# -*- coding: utf-8 -*-
import logging

import requests

from django.conf import settings
from django.template import response
from django.views.generic import base

from inscricao import forms, models
from lxml import etree

logger = logging.getLogger('devincachu.inscricoes')


class InscricaoView(base.View):
    templates = {
        u"fechadas": "inscricoes_fechadas.html",
        u"abertas": "inscricoes_abertas.html",
        u"encerradas": "inscricoes_encerradas.html",
    }

    def __init__(self, *args, **kwargs):
        super(InscricaoView, self).__init__(*args, **kwargs)
        self._configuracao = None

    @property
    def configuracao(self):
        if not self._configuracao:
            self._configuracao = models.Configuracao.objects.get()

        return self._configuracao

    def get(self, request):
        contexto = self.obter_contexto(self.configuracao)
        return response.TemplateResponse(request, self.templates[self.configuracao.status], contexto)

    def obter_contexto(self, configuracao):
        status = configuracao.status
        nome_do_metodo = "obter_contexto_inscricoes_%s" % status
        metodo = getattr(self, nome_do_metodo, None)
        return metodo and metodo(configuracao) or {}

    def obter_contexto_inscricoes_abertas(self, configuracao):
        form = forms.ParticipanteForm()
        return {"form": form, "configuracao": configuracao}

    def gerar_cobranca(self, participante):
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        payload = settings.PAGSEGURO
        payload["itemAmount1"] = "%.2f" % self.configuracao.valor_inscricao
        response = requests.post(settings.PAGSEGURO_GATEWAY, data=payload, headers=headers)
        if response.ok:
            dom = etree.fromstring(response.content)
            codigo_checkout = dom.xpath("//code")[0].text
            return codigo_checkout
        else:
            logger.error("\n\n\n########## Erro na inscrição do participante %d - %s (%s) ##########" % (participante.pk, participante.nome, participante.email))
            logger.error("Erro na comunicação com PagSeguro: %s - %s" % (response.status_code, response.content))
            logger.error("#################################################################\n\n\n")
            return None

    def post(self, request):
        form = forms.ParticipanteForm(request.POST)
        if form.is_valid():
            participante = form.save()
            codigo_checkout = self.gerar_cobranca(participante)

            if codigo_checkout:
                checkout = models.Checkout.objects.create(codigo=codigo_checkout, participante=participante)
                return response.TemplateResponse(request, "aguardando_pagamento.html", {"checkout": checkout})

            return response.TemplateResponse(request, "falha_comunicacao_pagseguro.html", {"participante": participante})

        contexto = {"form": form, "configuracao": self.configuracao}
        return response.TemplateResponse(request, "inscricoes_abertas.html", contexto)
