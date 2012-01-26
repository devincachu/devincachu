# -*- coding: utf-8 -*-

from django.views.generic import list

from palestras import models


class PalestrantesView(list.ListView):
    context_object_name = 'palestrantes'
    model = models.Palestrante
    template_name = 'palestrantes.html'
    queryset = models.Palestrante.objects.all().order_by('nome')


class ProgramacaoView(list.ListView):
    context_object_name = 'palestras'
    model = models.Palestra
    template_name = 'programacao.html'
    queryset = models.Palestra.objects.all().order_by('inicio')
