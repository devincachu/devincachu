# -*- coding: utf-8 -*-

from django.conf import settings
from django.views.generic import detail, list

from palestras import models


class PalestrantesView(list.ListView):
    context_object_name = u"palestrantes"
    model = models.Palestrante
    template_name = u"palestrantes.html"
    queryset = models.Palestrante.objects.filter(listagem=True).order_by(u"nome")

    def get_context_data(self, **kwargs):
        context = super(PalestrantesView, self).get_context_data(**kwargs)
        context.update({
            u"keywords": u"dev in cachu, palestrantes, %s" % u", ".join([p.nome for p in context["palestrantes"]]),
            u"description": u"Palestrantes do Dev in Cachu 2012",
            u"canonical_url": u"%s/palestrantes/" % settings.BASE_URL
        })

        return context


class ProgramacaoView(list.ListView):
    context_object_name = u"palestras"
    model = models.Palestra
    template_name = u"programacao.html"
    queryset = models.Palestra.objects.all().order_by(u"inicio")

    def get_context_data(self, **kwargs):
        context = super(ProgramacaoView, self).get_context_data(**kwargs)
        context.update({
            u"keywords": u"devincachu, dev in cachu 2012, palestras, programação, desenvolvimento de software",
            u"description": u"Grade de programação do Dev in Cachu 2012",
            u"canonical_url": u"%s/programacao/" % settings.BASE_URL,
        })
        return context


class PalestraView(detail.DetailView):
    context_object_name = u"palestra"
    model = models.Palestra
    template_name = u"palestra.html"

    def get_queryset(self):
        slugs_palestrantes = self.kwargs[u"palestrantes"].split(u"/")
        return models.Palestra.objects.filter(slug=self.kwargs[u"slug"], palestrantes__slug__in=slugs_palestrantes).distinct(u"pk")

    def get_context_data(self, **kwargs):
        context = super(PalestraView, self).get_context_data(**kwargs)
        context.update({
            u"keywords": u"dev in cachu 2012, palestra, %s, %s" % (context[u"palestra"], context[u"palestra"].nomes_palestrantes().replace(u" e ", u", ")),
            u"description": context[u"palestra"].descricao,
            u"canonical_url": u"%s/programacao/%s/%s/" % (settings.BASE_URL, self.kwargs[u"palestrantes"], self.kwargs[u"slug"]),
        })
        return context
