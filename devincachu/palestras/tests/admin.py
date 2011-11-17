# -*- coding: utf-8 -*-
import unittest

from django.contrib import admin as django_admin
from django.test import client

from palestras import admin, forms, models


class PalestranteAdminTestCase(unittest.TestCase):

    def setUp(self):
        self.dados = {
            "nome": "Francisco Souza",
            "minicurriculo": "PMP (Professional Mario Player)",
            "foto": "anonymous.png",
            "twitter": "franciscosouza",
        }

        factory = client.RequestFactory()
        self.request = factory.post("/", self.dados)

    def test_model_Palestrante_deve_estar_registrado_no_site_do_admin(self):
        self.assertIn(models.Palestrante, django_admin.site._registry)

    def test_model_Palestrante_deve_estar_registrado_com_classe_PalestranteAdmin(self):
        self.assertIsInstance(django_admin.site._registry[models.Palestrante], admin.PalestranteAdmin)

    def test_PalestranteAdmin_deve_usar_PalestranteAdminForm(self):
        self.assertEquals(forms.PalestranteAdminForm, admin.PalestranteAdmin.form)

    def test_nome_deve_estar_na_listagem(self):
        self.assertIn('nome', admin.PalestranteAdmin.list_display)

    def test_slug_deve_estar_na_listagem(self):
        self.assertIn('slug', admin.PalestranteAdmin.list_display)

    def test_deve_ser_possivel_buscar_pelo_nome(self):
        self.assertIn('nome', admin.PalestranteAdmin.search_fields)

    def test_deve_gravar_palestrante_com_slug(self):
        palestrante = models.Palestrante(**self.dados)
        adm = admin.PalestranteAdmin(palestrante, None)
        adm.save_model(self.request, palestrante, None, None)
        self.assertIsNotNone(palestrante.pk)
        self.assertEquals("francisco-souza", palestrante.slug)
