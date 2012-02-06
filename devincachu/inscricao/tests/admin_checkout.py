# -*- coding: utf-8 -*-
import unittest

from django.contrib import admin as django_admin
from django.test import client

from inscricao import admin, models


class AdminCheckoutTestCase(unittest.TestCase):

    def setUp(self):
        factory = client.RequestFactory()
        self.request = factory.get("/admin/checkout")
        self.request.user = None

    def test_model_Checkout_deve_estar_registrado_no_admin(self):
        self.assertIn(models.Checkout, django_admin.site._registry)

    def test_model_Checkout_deve_estar_registrado_com_CheckoutAdmin(self):
        self.assertIsInstance(django_admin.site._registry[models.Checkout], admin.CheckoutAdmin)

    def test_deve_exibir_codigo_na_listagem(self):
        self.assertIn("codigo", admin.CheckoutAdmin.list_display)

    def test_deve_exibir_nome_do_participante_na_listagem(self):
        self.assertIn("nome_participante", admin.CheckoutAdmin.list_display)

    def test_deve_exibir_email_do_participante_na_listagem(self):
        self.assertIn("email_participante", admin.CheckoutAdmin.list_display)

    def test_deve_ser_possivel_buscar_pelo_codigo(self):
        self.assertIn("codigo", admin.CheckoutAdmin.search_fields)

    def test_deve_ser_possivel_buscar_pelo_nome_do_participante(self):
        self.assertIn("participante__nome", admin.CheckoutAdmin.search_fields)

    def test_deve_ser_possivel_buscar_pelo_email_do_participante(self):
        self.assertIn("participante__nome", admin.CheckoutAdmin.search_fields)

    def test_nome_participante_deve_retornar_nome_do_participante(self):
        participante = models.Participante(nome=u"Francisco Souza")
        checkout = models.Checkout(participante=participante)
        cadmin = admin.CheckoutAdmin(checkout, None)
        self.assertEquals(participante.nome, cadmin.nome_participante(checkout))

    def test_email_participante_deve_retornar_email_do_participante(self):
        participante = models.Participante(email=u"f@souza.cc")
        checkout = models.Checkout(participante=participante)
        cadmin = admin.CheckoutAdmin(checkout, None)
        self.assertEquals(participante.email, cadmin.email_participante(checkout))

    def test_nao_deve_ser_possivel_adicionar_checkouts_pelo_admin(self):
        cadmin = admin.CheckoutAdmin(models.Checkout(), None)
        self.assertFalse(cadmin.has_add_permission(self.request))
