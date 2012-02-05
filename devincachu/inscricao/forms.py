# -*- coding: utf-8 -*-
from django import forms

from inscricao import models


class ParticipanteForm(forms.ModelForm):
    error_css_class = u"erro"
    required_css_class = u"obrigatorio"

    class Meta:
        model = models.Participante
        exclude = ("confirmado",)
