# -*- coding: utf-8 -*-
from django import test
from django.template import response
from django.test import client
from django.views.generic import base
from lxml import html

from destaques import models, views


class IndexViewTestCase(test.TestCase):
    fixtures = ('destaques-e-chamadas.yaml',)

    def setUp(self):
        factory = client.RequestFactory()
        self.request = factory.get("/")
        self.view = views.IndexView()

    def test_view_deve_herdar_de_View(self):
        assert issubclass(views.IndexView, base.View)

    def test_metodo_obter_destaques_deve_trazer_apenas_instancias_de_Destaque_excluindo_Chamada(self):
        destaques = self.view.obter_destaques()
        for destaque in destaques:
            self.assertNotIsInstance(destaque, models.Chamada)

    def test_metodo_obter_destaque_deve_trazer_no_maximo_dez_destaques(self):
        destaques = self.view.obter_destaques()
        self.assertEquals(10, len(destaques))

    def test_metodo_obter_destaque_deve_trazer_destaques_mais_recentes(self):
        esperado = [
            u"Bill Gates confirma participação no Dev in Cachu 2021",
            u"Bill Gates confirma participação no Dev in Cachu 2020",
            u"Bill Gates confirma participação no Dev in Cachu 2019",
            u"Bill Gates confirma participação no Dev in Cachu 2018",
            u"Bill Gates confirma participação no Dev in Cachu 2017",
            u"Bill Gates confirma participação no Dev in Cachu 2016",
            u"Bill Gates confirma participação no Dev in Cachu 2015",
            u"Bill Gates confirma participação no Dev in Cachu 2014",
            u"Palestra sobre C++",
            u"Palestra sobre Java",
        ]

        destaques = [d.titulo for d in self.view.obter_destaques()]
        self.assertEquals(esperado, destaques)

    def test_metodo_obter_chamada_deve_retornar_uma_chamada(self):
        chamada = self.view.obter_chamada()
        self.assertIsInstance(chamada, models.Chamada)

    def test_metodo_obter_chamada_deve_retornar_chamada_mais_recente(self):
        chamada = self.view.obter_chamada()
        self.assertEquals(u"Dev in Cachu 2012", chamada.titulo)

    def test_metodo_get_deve_retornar_TemplateResponse(self):
        r = self.view.get(self.request)
        self.assertIsInstance(r, response.TemplateResponse)

    def test_metodo_get_deve_renderizar_template_index(self):
        r = self.view.get(self.request)
        self.assertEquals("index.html", r.template_name)

    def test_metodo_get_deve_colocar_resultado_do_metodo_obter_destaques_na_variavel_de_contexto_destaques(self):
        destaques = list(self.view.obter_destaques())
        r = self.view.get(self.request)
        self.assertEquals(destaques, list(r.context_data['destaques']))

    def test_metodo_get_deve_colocar_resultado_do_metodo_obter_chamada_na_variavel_de_contexto_chamada(self):
        chamada = models.Chamada.objects.get(pk=5)
        r = self.view.get(self.request)
        self.assertEquals(chamada, r.context_data['chamada'])

    def test_deve_exibir_div_de_chamada_quando_estiver_no_contexto(self):
        r = self.view.get(self.request)
        r.render()
        dom = html.fromstring(r.content)
        self.assertEquals(1, len(dom.xpath('//div[@class="hero-unit"]')))


class IndexViewSemDados(test.TestCase):

    def setUp(self):
        factory = client.RequestFactory()
        self.request = factory.get("/")
        self.view = views.IndexView()

    def test_metodo_obter_destaques_deve_retornar_lista_vazia_quando_nao_houver_dados(self):
        self.assertEquals(0, len(self.view.obter_destaques()))

    def test_metodo_obter_chamada_deve_retornar_None_quando_nao_houver_dados(self):
        self.assertIsNone(self.view.obter_chamada())

    def test_se_nao_houver_chamada_nao_deve_exibir_div(self):
        r = self.view.get(self.request)
        r.render()
        dom = html.fromstring(r.content)
        self.assertEquals([], dom.xpath('//div[@class="hero-unit"]'))
