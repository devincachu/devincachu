# -*- coding: utf-8 -*-
from django import forms

from palestras import models


class PalestranteAdminForm(forms.ModelForm):
    class Meta:
        model = models.Palestrante
        exclude = ('slug',)
        widgets = {
            'minicurriculo': forms.Textarea,
        }


class PalestraAdminForm(forms.ModelForm):
    class Meta:
        model = models.Palestra
        exclude = ('slug',)
        widgets = {
            'descricao': forms.Textarea,
        }
