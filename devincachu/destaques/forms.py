# -*- coding: utf-8 -*-
from django import forms

from destaques import models


class DestaqueAdminForm(forms.ModelForm):
    class Meta:
        model = models.Destaque
        exclude = ('autor', 'data')
        widgets = {
            'conteudo': forms.Textarea,
        }


class ChamadaAdminForm(forms.ModelForm):
    class Meta(DestaqueAdminForm.Meta):
        model = models.Chamada
