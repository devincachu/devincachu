# -*- coding: utf-8 -*-
from django.conf import settings
from django.template import response
from django.views.generic import base

from destaques import models


class IndexView(base.View):

    def obter_destaques(self):
        return models.Destaque.objects.select_related().filter(chamada__isnull=True).order_by('-data')[:14]

    def obter_chamada(self):
        chamadas = models.Chamada.objects.select_related().order_by('-data')[:1]

        if chamadas:
            return chamadas[0]

        return None

    def get(self, request):
        contexto = {
            'destaques': self.obter_destaques(),
            'chamada': self.obter_chamada(),
            'canonical_url': u"%s/" % settings.BASE_URL,
            'keywords': u"devincachu, dev in cachu 2012, evento de informática, desenvolvimento de software, cachoeiro de itapemirim",
            'description': u"Dev in Cachu 2012 - evento sobre desenvolvimento de software no sul do Espírito Santo",
        }

        return response.TemplateResponse(request, "index.html", contexto)
