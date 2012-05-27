# -*- coding: utf-8 -*-
import unittest

from django.contrib import admin as django_admin
from django.test import client

from inscricao import admin, models


class AdminParticipanteTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.participante = models.Participante.objects.create(
                nome=u"Francisco Souza",
                cidade=u"Cachoeiro de Itapemirim",
                sexo=u"M",
                email=u"francisco@devincachu.com.br",
                status=u"CONFIRMADO",
        )

    @classmethod
    def tearDownClass(cls):
        cls.participante.delete()

    def test_model_Participante_deve_estar_registrado_no_admin(self):
        self.assertIn(models.Participante, django_admin.site._registry)

    def test_model_Participante_deve_estar_registrado_com_a_classe_ParticipanteAdmin(self):
        self.assertIsInstance(django_admin.site._registry[models.Participante], admin.ParticipanteAdmin)

    def test_deve_exibir_nome_na_listagem(self):
        self.assertIn("nome", admin.ParticipanteAdmin.list_display)

    def test_deve_exibir_cidade_na_listagem(self):
        self.assertIn("cidade", admin.ParticipanteAdmin.list_display)

    def test_deve_exibir_sexo_na_listagem(self):
        self.assertIn("sexo", admin.ParticipanteAdmin.list_display)

    def test_deve_exibir_email_na_listagem(self):
        self.assertIn("email", admin.ParticipanteAdmin.list_display)

    def test_deve_exibir_empresa_na_listagem(self):
        self.assertIn("empresa", admin.ParticipanteAdmin.list_display)

    def test_deve_exibir_instituicao_ensino_na_listagem(self):
        self.assertIn("instituicao_ensino", admin.ParticipanteAdmin.list_display)

    def test_deve_exibir_tamanho_de_camiseta_na_listagem(self):
        self.assertIn("tamanho_camiseta", admin.ParticipanteAdmin.list_display)

    def test_deve_exibir_status_na_listagem(self):
        self.assertIn("status", admin.ParticipanteAdmin.list_display)

    def test_deve_exibir_se_estava_presente(self):
        self.assertIn("presente", admin.ParticipanteAdmin.list_display)

    def test_deve_permitir_buscar_pelo_nome(self):
        self.assertIn("nome", admin.ParticipanteAdmin.search_fields)

    def test_deve_permitir_buscar_pelo_email(self):
        self.assertIn("email", admin.ParticipanteAdmin.search_fields)

    def test_deve_permitir_filtrar_pelo_sexo(self):
        self.assertIn("sexo", admin.ParticipanteAdmin.list_filter)

    def test_deve_permitir_filtrar_pelo_tamanho_de_camiseta(self):
        self.assertIn("tamanho_camiseta", admin.ParticipanteAdmin.list_filter)

    def test_deve_permitir_filtrar_pelo_status(self):
        self.assertIn("status", admin.ParticipanteAdmin.list_filter)

    def test_deve_permitir_filtrar_os_presentes(self):
        self.assertIn("presente", admin.ParticipanteAdmin.list_filter)

    def test_action_confirma_presenca(self):
        factory = client.RequestFactory()
        request = factory.get("/admin/inscricao/participante/")
        qs = models.Participante.objects.filter(pk=self.participante.pk)
        mdladmin = admin.ParticipanteAdmin(models.Participante, django_admin.site)
        admin.confirmar_presenca(mdladmin, request, qs)
        p = models.Participante.objects.get(pk=self.participante.pk)
        self.assertTrue(p.presente)

    def test_action_confirma_presenca_descricao(self):
        self.assertEqual(u"Confirmar presença", admin.confirmar_presenca.short_description)

    def test_deve_ter_action_de_confirmar_presenca(self):
        self.assertIn(admin.confirmar_presenca, admin.ParticipanteAdmin.actions)
