# -*- coding: utf-8 -*-
import unittest

from django import forms as django_forms

from inscricao import models, forms


class ParticipanteFormTestCase(unittest.TestCase):

    def test_deve_ser_um_ModelForm(self):
        assert issubclass(forms.ParticipanteForm, django_forms.ModelForm)

    def test_model_deve_ser_Participante(self):
        self.assertEquals(models.Participante, forms.ParticipanteForm.Meta.model)

    def test_nao_deve_trazer_campo_confirmado_do_model(self):
        self.assertIn("confirmado", forms.ParticipanteForm.Meta.exclude)

    def test_deve_ter_estilo_para_campos_obrigatorios(self):
        self.assertEquals("obrigatorio", forms.ParticipanteForm.required_css_class)

    def test_deve_ter_estilo_para_campos_com_erro(self):
        self.assertEquals("error", forms.ParticipanteForm.error_css_class)
