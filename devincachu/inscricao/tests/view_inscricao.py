# -*- coding: utf-8 -*-
import unittest

from django.test import client

from inscricao import models, views


class ViewInscricaoTestCase(unittest.TestCase):

    def setUp(self):
        factory = client.RequestFactory()
        self.request = factory.get("/inscricoes/")

    def test_deve_ter_dicionario_com_templates_para_cada_status(self):
        esperado = {
            u"fechadas": "inscricoes_fechadas.html",
            u"abertas": "inscricoes_abertas.html",
            u"encerradas": "inscricoes_encerradas.html",
        }
        self.assertEquals(esperado, views.InscricaoView.templates)

    def test_deve_renderizar_template_inscricoes_fechadas_para_status_inscricoes_fechadas(self):
        configuracao = models.Configuracao.objects.get()
        assert configuracao.status == "fechadas"

        view = views.InscricaoView()
        response = view.get(self.request)
        self.assertEquals(u"inscricoes_fechadas.html", response.template_name)
