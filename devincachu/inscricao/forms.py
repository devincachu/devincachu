# -*- coding: utf-8 -*-
from django import forms

from inscricao import models


class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = models.Participante
        exclude = ("confirmado",)
