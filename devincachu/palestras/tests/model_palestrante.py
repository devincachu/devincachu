# -*- coding: utf-8 -*-
import unittest

from django.db import models as django_models

from palestras import models


class ModelPalestranteTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.field_names = [f.name for f in models.Palestrante._meta.fields]

    def test_model_palestrante_deve_ter_nome(self):
        self.assertIn('nome', self.field_names)

    def test_campo_nome_deve_ser_CharField(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'nome'][0]
        self.assertIsInstance(field, django_models.CharField)

    def test_campo_nome_nao_deve_aceitar_blank(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'nome'][0]
        self.assertFalse(field.blank)

    def test_campo_nome_deve_ter_no_maximo_100_caracteres(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'nome'][0]
        self.assertEquals(100, field.max_length)

    def test_model_palestrante_deve_ter_blog(self):
        self.assertIn('blog', self.field_names)

    def test_campo_blog_deve_ser_URLField(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'blog'][0]
        self.assertIsInstance(field, django_models.URLField)

    def test_campo_blog_deve_aceitar_blank(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'blog'][0]
        self.assertTrue(field.blank)

    def test_campo_blog_deve_ter_verify_false(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'blog'][0]
        validator = field.validators[1]
        self.assertFalse(validator.verify_exists)

    def test_campo_blog_deve_ter_no_maximo_255_caracteres(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'blog'][0]
        self.assertEquals(255, field.max_length)

    def test_model_palestrante_deve_ter_campo_para_perfil_no_twitter(self):
        self.assertIn('twitter', self.field_names)

    def test_campo_twitter_deve_ser_CharField(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'twitter'][0]
        self.assertIsInstance(field, django_models.CharField)

    def test_campo_twitter_deve_aceitar_blank(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'twitter'][0]
        self.assertTrue(field.blank)

    def test_campo_twitter_deve_ter_no_maximo_50_caracteres(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'twitter'][0]
        self.assertEquals(50, field.max_length)

    def test_model_palestrante_deve_ter_campo_para_minicurriculo(self):
        self.assertIn('minicurriculo', self.field_names)

    def test_campo_minicurriculo_deve_ser_CharField(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'minicurriculo'][0]
        self.assertIsInstance(field, django_models.CharField)

    def test_campo_minicurriculo_nao_deve_aceitar_blank(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'minicurriculo'][0]
        self.assertFalse(field.blank)

    def test_campo_minicurriculo_deve_ter_no_maximo_500_caracteres(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'minicurriculo'][0]
        self.assertEquals(500, field.max_length)

    def test_palestrante_deve_ter_foto(self):
        self.assertIn('foto', self.field_names)

    def test_campo_foto_deve_ser_do_tipo_ImageField(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'foto'][0]
        self.assertIsInstance(field, django_models.ImageField)

    def test_campo_foto_deve_enviar_fotos_para_diretorio_palestrantes(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'foto'][0]
        self.assertEquals("palestrantes", field.upload_to)

    def test_campo_foto_nao_deve_aceitar_blank(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'foto'][0]
        self.assertFalse(field.blank)
