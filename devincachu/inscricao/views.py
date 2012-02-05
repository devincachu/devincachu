# -*- coding: utf-8 -*-
from django.template import response
from django.views.generic import base

from inscricao import forms, models


class InscricaoView(base.View):
    templates = {
        u"fechadas": "inscricoes_fechadas.html",
        u"abertas": "inscricoes_abertas.html",
        u"encerradas": "inscricoes_encerradas.html",
    }

    def get(self, request):
        configuracao = models.Configuracao.objects.get()
        contexto = self.obter_contexto(configuracao)
        return response.TemplateResponse(request, self.templates[configuracao.status], contexto)

    def obter_contexto(self, configuracao):
        status = configuracao.status
        nome_do_metodo = "obter_contexto_inscricoes_%s" % status
        metodo = getattr(self, nome_do_metodo, None)
        return metodo and metodo(configuracao) or {}

    def obter_contexto_inscricoes_abertas(self, configuracao):
        form = forms.ParticipanteForm()
        return {"form": form, "configuracao": configuracao}
