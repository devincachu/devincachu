# -*- coding: utf-8 -*-
import unittest

from django.contrib import admin as django_admin

from inscricao import admin, models


class AdminParticipanteTestCase(unittest.TestCase):

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
