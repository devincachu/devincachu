# -*- coding: utf-8 -*-
import unittest

from django.core import management
from django.test import client
from django.views.generic import list

from palestras import models, views


class ProgramacaoViewTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        management.call_command("loaddata", "palestrantes.yaml", verbosity=0)
        management.call_command("loaddata", "palestras.yaml", verbosity=0)

    @classmethod
    def tearDownClass(cls):
        management.call_command("flush", verbosity=0, interactive=False)

    def setUp(self):
        factory = client.RequestFactory()
        self.request = factory.get("/programacao")

    def test_deve_herdar_de_ListView(self):
        assert issubclass(views.ProgramacaoView, list.ListView)

    def test_deve_usar_model_Palestra(self):
        self.assertEquals(models.Palestra, views.ProgramacaoView.model)

    def test_deve_ter_context_object_name_para_palestras(self):
        self.assertEquals("palestras", views.ProgramacaoView.context_object_name)

    def test_deve_trazer_palestras_no_contexto_ordenadas_pelo_horario_de_inicio(self):
        view = views.ProgramacaoView.as_view()
        response = view(self.request)
        palestras = response.context_data["palestras"]

        titulos_esperados = [u"Recepção e credenciamento", u"Escalando aplicações Django", "Arquitetura escalável de aplicação de alto desempenho", u"Almoço"]
        titulos_obtidos = [p.titulo for p in palestras]
        self.assertEquals(titulos_esperados, titulos_obtidos)
