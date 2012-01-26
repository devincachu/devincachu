# -*- coding: utf-8 -*-

from django.views.generic import detail, list

from palestras import models


class PalestrantesView(list.ListView):
    context_object_name = "palestrantes"
    model = models.Palestrante
    template_name = "palestrantes.html"
    queryset = models.Palestrante.objects.all().order_by("nome")


class ProgramacaoView(list.ListView):
    context_object_name = "palestras"
    model = models.Palestra
    template_name = "programacao.html"
    queryset = models.Palestra.objects.all().order_by("inicio")


class PalestraView(detail.DetailView):
    context_object_name = "palestra"
    model = models.Palestra
    template_name = "palestra.html"

    def get_queryset(self):
        slugs_palestrantes = self.kwargs["palestrantes"].split("/")
        return models.Palestra.objects.filter(slug=self.kwargs["slug"], palestrantes__slug__in=slugs_palestrantes).distinct("pk")
