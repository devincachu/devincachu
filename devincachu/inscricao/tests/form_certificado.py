# -*- coding: utf-8 -*-
import unittest

from django import forms as django_forms

from inscricao import forms


class FormValidacaoCertificadoTestCase(unittest.TestCase):

    def test_deve_ser_um_form(self):
        assert issubclass(forms.ValidacaoCertificado, django_forms.Form)

    def test_error_css_class_deve_ser_error(self):
        self.assertEqual(u"error", forms.ValidacaoCertificado.error_css_class)

    def test_deve_ter_campo_codigo_certificado(self):
        self.assertIn("codigo", forms.ValidacaoCertificado.base_fields)

    def test_campo_codigo_deve_ser_CharField(self):
        f = forms.ValidacaoCertificado.base_fields["codigo"]
        self.assertIsInstance(f, django_forms.CharField)

    def test_campo_codigo_deve_ter_no_maximo_30_caracteres(self):
        f = forms.ValidacaoCertificado.base_fields["codigo"]
        self.assertEqual(f.max_length, 30)
