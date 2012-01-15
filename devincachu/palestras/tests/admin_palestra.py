# -*- coding: utf-8 -*-
import unittest

from django.contrib import admin as django_admin
from django.core import management
from django.test import client

from palestras import admin, forms, models


class AdminPalestraTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        management.call_command("loaddata", "palestrantes.yaml", verbosity=0)

    @classmethod
    def tearDownClass(cls):
        management.call_command("flush", interactive=False, verbosity=0)

    def setUp(self):
        self.dados = {
            "titulo": u"Aprendendo Python",
            "descricao": u"Venha aprender Python!",
            "inicio": u"09:00:00",
            "termino": u"10:00:00",
        }

        factory = client.RequestFactory()
        self.request = factory.post("/", self.dados)

        models.Palestra.objects.filter(**self.dados).delete()

    def test_model_Palestra_deve_estar_registrado_no_site_do_admin(self):
        self.assertIn(models.Palestra, django_admin.site._registry)

    def test_model_Palestra_deve_estar_registrado_com_classe_PalestraAdmin(self):
        self.assertIsInstance(django_admin.site._registry[models.Palestra], admin.PalestraAdmin)

    def test_PalestraAdmin_deve_usar_PalestraAdminForm(self):
        self.assertEquals(forms.PalestraAdminForm, admin.PalestraAdmin.form)

    def test_titulo_deve_estar_listagem(self):
        self.assertIn('titulo', admin.PalestraAdmin.list_display)

    def test_slug_deve_estar_na_listagem(self):
        self.assertIn('slug', admin.PalestraAdmin.list_display)

    def test_palestrantes_deve_estar_na_listagem(self):
        self.assertIn('nomes_palestrantes', admin.PalestraAdmin.list_display)

    def test_hora_de_inicio_deve_estar_na_listagem(self):
        self.assertIn('inicio', admin.PalestraAdmin.list_display)

    def test_deve_ser_possivel_buscar_pelo_titulo_da_palestra(self):
        self.assertIn("titulo", admin.PalestraAdmin.search_fields)

    def test_deve_ser_possivel_filtrar_pelo_palestrante(self):
        self.assertIn("palestrantes", admin.PalestraAdmin.list_filter)

    def test_deve_salvar_palestra_com_slug(self):
        palestra = models.Palestra(**self.dados)
        adm = admin.PalestraAdmin(palestra, None)
        adm.save_model(self.request, palestra, None, None)
        self.assertIsNotNone(palestra.pk)
        self.assertEquals("aprendendo-python", palestra.slug)

    def test_metodo_palestrantes_do_admin_deve_trazer_nomes_de_palestrantes_separados_por_virgula(self):
        palestra = models.Palestra(**self.dados)
        adm = admin.PalestraAdmin(palestra, None)
        adm.save_model(self.request, palestra, None, None)
        palestra.palestrantes = models.Palestrante.objects.filter(pk__lt=4)
        palestra.save()

        self.assertEquals(u"Hannibal Lecter, James Bond, Vito Corleone", adm.nomes_palestrantes(palestra))

    def test_metodo_palestrantes_deve_ter_short_description_indicando_singular_ou_plural(self):
        self.assertEquals(u"Palestrante(s)", admin.PalestraAdmin.nomes_palestrantes.short_description)
