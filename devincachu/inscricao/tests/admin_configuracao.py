# -*- coding: utf-8 -*-
import unittest

from django.contrib import admin as django_admin
from django.test import client

from inscricao import admin, models


class ConfiguracaoAdminTestCase(unittest.TestCase):

    def setUp(self):
        factory = client.RequestFactory()
        self.request = factory.get("/admin/configuracao/add")
        self.request.user = None

    def test_model_Configuracao_deve_estar_registrado_no_admin(self):
        self.assertIn(models.Configuracao, django_admin.site._registry)

    def test_model_Configuracao_deve_estar_registrado_com_classe_ConfiguracaoAdmin(self):
        self.assertIsInstance(django_admin.site._registry[models.Configuracao], admin.ConfiguracaoAdmin)

    def test_nao_deve_ser_possivel_adicionar_uma_instancia_pelo_admin(self):
        cadmin = admin.ConfiguracaoAdmin(models.Configuracao.objects.get(), None)
        self.assertFalse(cadmin.has_add_permission(self.request))

    def test_nao_deve_ser_possivel_apagar_uma_instancia_pelo_admin(self):
        cadmin = admin.ConfiguracaoAdmin(models.Configuracao.objects.get(), None)
        self.assertFalse(cadmin.has_delete_permission(self.request))
