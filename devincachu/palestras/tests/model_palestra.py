# -*- coding: utf-8 -*-
import unittest

from django.core import management
from django.db import models as django_models

from palestras import models


class ModelPalestraTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        management.call_command("loaddata", "palestrantes.yaml", verbosity=0)
        management.call_command("loaddata", "palestras.yaml", verbosity=0)
        cls.field_names = models.Palestra._meta.get_all_field_names()

    @classmethod
    def tearDownClass(cls):
        management.call_command("flush", verbosity=0, interactive=False)

    def test_model_palestra_deve_ter_titulo(self):
        self.assertIn("titulo", self.field_names)

    def test_titulo_deve_ser_CharField(self):
        field = models.Palestra._meta.get_field_by_name("titulo")[0]
        self.assertIsInstance(field, django_models.CharField)

    def test_titulo_deve_ter_no_maximo_150_caracteres(self):
        field = models.Palestra._meta.get_field_by_name("titulo")[0]
        self.assertEquals(150, field.max_length)

    def test_titulo_deve_ter_verbose_name_com_caractere_especial(self):
        field = models.Palestra._meta.get_field_by_name("titulo")[0]
        self.assertEquals(u"Título", field.verbose_name)

    def test_model_palestra_deve_ter_slug(self):
        self.assertIn("slug", self.field_names)

    def test_slug_deve_ser_SlugField(self):
        field = models.Palestra._meta.get_field_by_name("slug")[0]
        self.assertIsInstance(field, django_models.SlugField)

    def test_slug_deve_ter_no_maximo_150_caracteres(self):
        field = models.Palestra._meta.get_field_by_name("slug")[0]
        self.assertEquals(150, field.max_length)

    def test_slug_deve_ser_unico(self):
        field = models.Palestra._meta.get_field_by_name("slug")[0]
        self.assertTrue(field.unique)

    def test_model_palestra_deve_ter_descricao(self):
        self.assertIn("descricao", self.field_names)

    def test_descricao_deve_ser_CharField(self):
        field = models.Palestra._meta.get_field_by_name("descricao")[0]
        self.assertIsInstance(field, django_models.CharField)

    def test_descricao_deve_ter_no_maximo_1000_caracteres(self):
        field = models.Palestra._meta.get_field_by_name("descricao")[0]
        self.assertEquals(1000, field.max_length)

    def test_descricao_deve_ter_verbose_name_com_caracteres_especiais(self):
        field = models.Palestra._meta.get_field_by_name("descricao")[0]
        self.assertEquals(u"Descrição", field.verbose_name)

    def test_model_palestra_deve_ter_hora_de_inicio(self):
        self.assertIn("inicio", self.field_names)

    def test_inicio_deve_ser_do_tipo_TimeField(self):
        field = models.Palestra._meta.get_field_by_name("inicio")[0]
        self.assertIsInstance(field, django_models.TimeField)

    def test_inicio_deve_ter_verbose_name_descritivo(self):
        field = models.Palestra._meta.get_field_by_name("inicio")[0]
        self.assertEquals(u"Horário de início", field.verbose_name)

    def test_model_palestra_deve_ter_hora_de_termino(self):
        self.assertIn("termino", self.field_names)

    def test_termino_deve_ser_do_tipo_TimeField(self):
        field = models.Palestra._meta.get_field_by_name("termino")[0]
        self.assertIsInstance(field, django_models.TimeField)

    def test_termino_dve_ter_verbose_name_descritivo(self):
        field = models.Palestra._meta.get_field_by_name("termino")[0]
        self.assertEquals(u"Horário de término", field.verbose_name)

    def test_model_palestra_deve_ter_campo_palestrantes(self):
        self.assertIn("palestrantes", self.field_names)

    def test_palestrantes_deve_ser_um_ManyToManyField(self):
        field = models.Palestra._meta.get_field_by_name("palestrantes")[0]
        self.assertIsInstance(field, django_models.ManyToManyField)

    def test_palestrantes_deve_apontar_para_model_Palestrante(self):
        field = models.Palestra._meta.get_field_by_name("palestrantes")[0]
        self.assertEquals(models.Palestrante, field.related.parent_model)

    def test_palestrantes_deve_aceitar_blank(self):
        field = models.Palestra._meta.get_field_by_name("palestrantes")[0]
        self.assertTrue(field.blank)

    def test_nomes_palestrantes_deve_retornar_nomes_dos_palestrantes_com_virgula_e_e(self):
        palestra = models.Palestra.objects.get(pk=1)
        self.assertEquals(u"Hannibal Lecter e Vito Corleone", palestra.nomes_palestrantes())

    def test_deve_ter_representacao_simples_que_utilize_titulo_da_palestra(self):
        palestra = models.Palestra(titulo=u"Testando aplicações web")
        self.assertEquals('<Palestra: Testando aplicações web>', repr(palestra))

    def test_deve_exibir_titulo_como_unicode(self):
        palestra = models.Palestra(titulo=u"Testando aplicações web")
        self.assertEquals(palestra.titulo, unicode(palestra))

    def test_get_absolute_url_deve_retornar_url_para_palestra_quando_a_palestra_tem_palestrante(self):
        palestra = models.Palestra.objects.get(pk=1)
        url_esperada = "/programacao/hannibal-lecter/vito-corleone/%s/" % palestra.slug
        self.assertEquals(url_esperada, palestra.get_absolute_url_and_link_title()['url'])

    def test_get_absolute_url_deve_retornar_tralha_quando_a_palestra_nao_tem_palestrante(self):
        palestra = models.Palestra.objects.get(pk=2)
        self.assertEquals("#", palestra.get_absolute_url_and_link_title()['url'])

    def test_link_title_deve_retornar_descricao_da_palestra_quando_a_palestra_nao_tem_palestrante(self):
        palestra = models.Palestra.objects.get(pk=2)
        self.assertEquals(palestra.descricao, palestra.get_absolute_url_and_link_title()['title'])

    def test_link_title_deve_retornar_chamada_da_palestra_com_nomes_dos_palestrantes_no_plural(self):
        palestra = models.Palestra.objects.get(pk=1)
        esperado = u"Veja mais informações da palestra %s e dos palestrantes %s" % (palestra.titulo, palestra.nomes_palestrantes())
        self.assertEquals(esperado, palestra.get_absolute_url_and_link_title()['title'])

    def test_link_title_deve_retornar_chamada_da_palestra_com_nome_no_singular_quando_tem_apenas_um_palestrante(self):
        palestra = models.Palestra.objects.get(pk=3)
        esperado = u"Veja mais informações da palestra %s e do palestrante %s" % (palestra.titulo, palestra.nomes_palestrantes())
        self.assertEquals(esperado, palestra.get_absolute_url_and_link_title()['title'])
