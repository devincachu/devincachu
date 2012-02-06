# -*- coding: utf-8 -*-
import unittest

from django.db import models as django_models

from inscricao import models


class CheckoutTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.field_names = models.Checkout._meta.get_all_field_names()

    def test_deve_ter_codigo(self):
        self.assertIn("codigo", self.field_names)

    def test_codigo_deve_ser_do_tipo_CharField(self):
        field = models.Checkout._meta.get_field_by_name("codigo")[0]
        self.assertIsInstance(field, django_models.CharField)

    def test_codigo_deve_ter_no_maximo_100_caracteres(self):
        field = models.Checkout._meta.get_field_by_name("codigo")[0]
        self.assertEquals(100, field.max_length)

    def test_deve_ter_campo_participante(self):
        self.assertIn("participante", self.field_names)

    def test_participante_deve_ser_FK(self):
        field = models.Checkout._meta.get_field_by_name("participante")[0]
        self.assertIsInstance(field, django_models.ForeignKey)

    def test_participante_deve_apontar_para_model_Participante(self):
        field = models.Checkout._meta.get_field_by_name("participante")[0]
        self.assertEquals(models.Participante, field.related.parent_model)

    def test__unicode__deve_retornar_codigo_e_nome_do_participante(self):
        participante = models.Participante(nome=u"Francisco Souza", email="chico@devincachu.com.br")
        checkout = models.Checkout(codigo=u"123", participante=participante)
        self.assertEquals(u"123 (Francisco Souza - chico@devincachu.com.br)", unicode(checkout))
