# -*- coding: utf-8 -*-
from django.template import response
from django.views.generic import base

from inscricao import models


class InscricaoView(base.View):
    templates = {
        u"fechadas": "inscricoes_fechadas.html",
        u"abertas": "inscricoes_abertas.html",
        u"encerradas": "inscricoes_encerradas.html",
    }

    def get(self, request):
        configuracao = models.Configuracao.objects.get()
        return response.TemplateResponse(request, self.templates[configuracao.status])
