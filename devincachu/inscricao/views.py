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

    def post(self, request):
        form = forms.ParticipanteForm(request.POST)
        if not form.is_valid():
            contexto = {"form": form, "configuracao": self.configuracao}
            return response.TemplateResponse(request, "inscricoes_abertas.html", contexto)
