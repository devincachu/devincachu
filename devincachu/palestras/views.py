# -*- coding: utf-8 -*-

from django.views.generic import list

from palestras import models


class PalestrantesView(list.ListView):
    context_object_name = 'palestrantes'
    model = models.Palestrante
    template_name = 'palestrantes.html'
