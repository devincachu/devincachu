# -*- coding: utf-8 -*-
import unittest

from django.test import client

from inscricao import forms, models, views


class ViewInscricaoInscricoesFechadasTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        factory = client.RequestFactory()
        request = factory.get("/inscricoes/")
        configuracao = models.Configuracao.objects.get()
        configuracao.status = "fechadas"
        configuracao.save()

        view = views.InscricaoView()
        cls.response = view.get(request)

    def test_deve_ter_dicionario_com_templates_para_cada_status(self):
        esperado = {
            u"fechadas": "inscricoes_fechadas.html",
            u"abertas": "inscricoes_abertas.html",
            u"encerradas": "inscricoes_encerradas.html",
        }
        self.assertEquals(esperado, views.InscricaoView.templates)

    def test_deve_renderizar_template_inscricoes_fechadas_para_status_inscricoes_fechadas(self):
        self.assertEquals(u"inscricoes_fechadas.html", self.response.template_name)

    def test_deve_ter_contexto_vazio(self):
        self.assertEquals({}, self.response.context_data)


class ViewInscricaoInscricoesAbertasTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        factory = client.RequestFactory()
        request = factory.get("/inscricoes/")

        configuracao = models.Configuracao.objects.get()
        configuracao.status = "abertas"
        configuracao.save()

        view = views.InscricaoView()
        cls.response = view.get(request)

    def test_deve_renderizar_template_inscricoes_abertas_para_status_inscricoes_abertas(self):
        self.assertEquals(u"inscricoes_abertas.html", self.response.template_name)

    def test_deve_incluir_instancia_de_ParticipanteForm_no_contexto(self):
        context_data = self.response.context_data
        self.assertIsInstance(context_data["form"], forms.ParticipanteForm)
