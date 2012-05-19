# -*- coding: utf-8 -*-
from django import forms

from inscricao import models


class ParticipanteForm(forms.ModelForm):
    error_css_class = u"error"
    required_css_class = u"obrigatorio"

    class Meta:
        model = models.Participante
        exclude = ("status",)


class ValidacaoCertificado(forms.Form):
    codigo = forms.CharField(max_length=30)
    error_css_class = u"error"

    def obter_certificado(self):
        if self.is_valid():
            try:
                return models.Certificado.objects.select_related("participante").get(codigo=self.cleaned_data["codigo"])
            except models.Certificado.DoesNotExist:
                return None
