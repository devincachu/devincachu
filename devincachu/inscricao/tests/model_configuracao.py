# -*- coding: utf-8 -*-
import unittest

from django.db import models as django_models

from inscricao import models


class ConfiguracaoTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.field_names = models.Configuracao._meta.get_all_field_names()

    def test_deve_ter_campo_com_valor_da_inscricao(self):
        self.assertIn("valor_inscricao", self.field_names)

    def test_valor_da_inscricao_deve_ser_do_tipo_FloatField(self):
        field = models.Configuracao._meta.get_field_by_name("valor_inscricao")[0]
        self.assertIsInstance(field, django_models.FloatField)

    def test_valor_da_inscricao_deve_ter_verbose_name_com_special_chars(self):
        field = models.Configuracao._meta.get_field_by_name("valor_inscricao")[0]
        self.assertEquals(u"Valor da inscrição", field.verbose_name)

    def test_deve_ter_campo_informando_se_a_inscricao_esta_aberta(self):
        self.assertIn("status", self.field_names)

    def test_status_deve_ser_do_tipo_CharField(self):
        field = models.Configuracao._meta.get_field_by_name("status")[0]
        self.assertIsInstance(field, django_models.CharField)

    def test_status_deve_ter_no_maximo_10_caracteres(self):
        field = models.Configuracao._meta.get_field_by_name("status")[0]
        self.assertEquals(10, field.max_length)

    def test_status_deve_ser_fechadas_abertas_ou_encerradas(self):
        esperado = (
            (u"fechadas", u"Fechadas (inscrições ainda não abriram)"),
            (u"abertas", u"Inscrições abertas"),
            (u"encerradas", u"Inscrições encerradas"),
        )
        field = models.Configuracao._meta.get_field_by_name("status")[0]
        self.assertEquals(esperado, field.choices)

    def test__unicode__deve_retornar_informando_que_eh_model_de_configuracao_de_inscricao(self):
        configuracao = models.Configuracao.objects.get()
        self.assertEquals(u"Configuração das inscrições do Dev in Cachu 2012", unicode(configuracao))

    def test_verbose_name_deve_ter_acento_e_cedilha(self):
        self.assertEquals(u"Configuração das inscrições", models.Configuracao._meta.verbose_name)

    def test_verbose_name_plural_deve_ser_igual_verbose_name(self):
        self.assertEquals(models.Configuracao._meta.verbose_name, models.Configuracao._meta.verbose_name_plural)
