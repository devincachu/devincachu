# -*- coding: utf-8 -*-

from django.conf import settings
from django.views.generic import detail, list

from palestras import models


class PalestrantesView(list.ListView):
    context_object_name = "palestrantes"
    model = models.Palestrante
    template_name = "palestrantes.html"
    queryset = models.Palestrante.objects.all().order_by("nome")

    def get_context_data(self, **kwargs):
        context = super(PalestrantesView, self).get_context_data(**kwargs)
        context.update({
            u"keywords": u"dev in cachu, palestrantes, %s" % ", ".join([p.nome for p in context["palestrantes"]]),
            u"description": u"Palestrantes do Dev in Cachu 2012",
            u"canonical_url": "%s/palestrantes/" % settings.BASE_URL
        })

        return context


class ProgramacaoView(list.ListView):
    context_object_name = "palestras"
    model = models.Palestra
    template_name = "programacao.html"
    queryset = models.Palestra.objects.all().order_by("inicio")

    def get_context_data(self, **kwargs):
        context = super(ProgramacaoView, self).get_context_data(**kwargs)
        context.update({
            u"keywords": u"devincachu, dev in cachu 2012, palestras, programação, desenvolvimento de software",
            u"description": u"Grade de programação do Dev in Cachu 2012",
            u"canonical_url": "%s/programacao/" % settings.BASE_URL,
        })
        return context


class PalestraView(detail.DetailView):
    context_object_name = "palestra"
    model = models.Palestra
    template_name = "palestra.html"

    def get_queryset(self):
        slugs_palestrantes = self.kwargs["palestrantes"].split("/")
        return models.Palestra.objects.filter(slug=self.kwargs["slug"], palestrantes__slug__in=slugs_palestrantes).distinct("pk")

    def get_context_data(self, **kwargs):
        context = super(PalestraView, self).get_context_data(**kwargs)
        context.update({
            u"keywords": "dev in cachu 2012, palestra, %s, %s" % (context["palestra"], context["palestra"].nomes_palestrantes().replace(" e ", ", ")),
            u"description": context["palestra"].descricao,
            u"canonical_url": "%s/programacao/%s/%s/" % (settings.BASE_URL, self.kwargs["palestrantes"], self.kwargs["slug"]),
        })
        return context
