# -*- coding: utf-8 -*-
import unittest

from django import forms as django_forms

from palestras import forms, models


class PalestranteAdminFormTestCase(unittest.TestCase):

    def test_PalestranteAdminForm_deve_ser_um_ModelForm(self):
        assert issubclass(forms.PalestranteAdminForm, django_forms.ModelForm)

    def test_PalestranteAdminForm_deve_ter_model_Palestrante_no_meta(self):
        self.assertEquals(models.Palestrante, forms.PalestranteAdminForm.Meta.model)

    def test_PalestranteAdminForm_deve_excluir_campo_slug(self):
        self.assertIn('slug', forms.PalestranteAdminForm.Meta.exclude)

    def test_deve_utilizar_widget_de_textarea_para_minicurriculo(self):
        self.assertEquals(django_forms.Textarea, forms.PalestranteAdminForm.Meta.widgets['minicurriculo'])
