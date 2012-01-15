# -*- coding: utf-8 -*-
import unittest

from django.contrib import admin as django_admin

from palestras import admin, forms, models


class AdminPalestraTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_model_Palestra_deve_estar_registrado_no_site_do_admin(self):
        self.assertIn(models.Palestra, django_admin.site._registry)

    def test_model_Palestra_deve_estar_registrado_com_classe_PalestraAdmin(self):
        self.assertIsInstance(django_admin.site._registry[models.Palestra], admin.PalestraAdmin)

    def test_PalestraAdmin_deve_usar_PalestraAdminForm(self):
        self.assertEquals(forms.PalestraAdminForm, admin.PalestraAdmin.form)

    def test_titulo_deve_estar_listagem(self):
        self.assertIn('titulo', admin.PalestraAdmin.list_display)

    def test_slug_deve_estar_na_listage(self):
        self.assertIn('slug', admin.PalestraAdmin.list_display)

    def test_description_hora_de_inicio_deve_estar_na_listagem(self):
        self.assertIn('inicio', admin.PalestraAdmin.list_display)

    def test_deve_ser_possivel_buscar_pelo_titulo_da_palestra(self):
        self.assertIn("titulo", admin.PalestraAdmin.search_fields)

    def test_deve_ser_possivel_filtrar_pelo_palestrante(self):
        self.assertIn("palestrantes", admin.PalestraAdmin.list_filter)
