# -*- coding: utf-8 -*-
import unittest

from django.conf import settings
from django.core import management, urlresolvers
from django.template import response
from django.test import client
from django.views.generic import base
from lxml import html

from destaques import models, views


class IndexViewTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        management.call_command("loaddata", "destaques-e-chamadas.yaml", verbosity=0)

    @classmethod
    def tearDownClass(cls):
        management.call_command("flush", interactive=False, verbosity=0)

    def setUp(self):
        factory = client.RequestFactory()
        self.request = factory.get("/")
        self.view = views.IndexView()

    def test_view_deve_herdar_de_View(self):
        assert issubclass(views.IndexView, base.View)

    def test_deve_responder_pela_url_raiz(self):
        f = views.IndexView.as_view()
        r = urlresolvers.resolve('/')
        self.assertEquals(f.func_name, r.func.func_name)

    def test_metodo_obter_destaques_deve_trazer_apenas_instancias_de_Destaque_excluindo_Chamada(self):
        destaques = self.view.obter_destaques()
        for destaque in destaques:
            self.assertNotIsInstance(destaque, models.Chamada)

    def test_metodo_obter_destaque_deve_trazer_no_maximo_quatorze_destaques(self):
        destaques = self.view.obter_destaques()
        self.assertEquals(14, len(destaques))

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
            u"Palestra sobre C#",
            u"Palestra sobre Python",
            u"Bill Gates confirma participação no Dev in Cachu 2013",
            u"Bill Gates confirma participação no Dev in Cachu 2012",
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

    def test_deve_ter_canonical_url_da_home(self):
        r = self.view.get(self.request)
        r.render()
        dom = html.fromstring(r.content)
        esperado = "%s/" % settings.BASE_URL
        self.assertEquals(esperado, dom.xpath('//link[@rel="canonical"]')[0].attrib["href"])

    def test_meta_keywords(self):
        r = self.view.get(self.request)
        r.render()
        dom = html.fromstring(r.content)
        esperado = u"devincachu, dev in cachu 2012, evento de informática, desenvolvimento de software, cachoeiro de itapemirim"
        self.assertEquals(esperado, dom.xpath('//meta[@name="keywords"]')[0].attrib["content"].encode("iso-8859-1"))

    def test_meta_description(self):
        r = self.view.get(self.request)
        r.render()
        dom = html.fromstring(r.content)
        esperado = u"Dev in Cachu 2012 - evento sobre desenvolvimento de software no sul do Espírito Santo"
        self.assertEquals(esperado, dom.xpath('//meta[@name="description"]')[0].attrib["content"].encode("iso-8859-1"))

    def test_og_title_deve_ter_nome_e_edicao_do_evento(self):
        r = self.view.get(self.request)
        r.render()
        dom = html.fromstring(r.content)
        esperado = u"Dev in Cachu 2012"
        self.assertEquals(esperado, dom.xpath('//meta[@property="og:title"]')[0].attrib["content"].encode("iso-8859-1"))

    def test_og_type_deve_ser_website(self):
        r = self.view.get(self.request)
        r.render()
        dom = html.fromstring(r.content)
        esperado = u"website"
        self.assertEquals(esperado, dom.xpath('//meta[@property="og:type"]')[0].attrib["content"].encode("iso-8859-1"))

    def test_og_url_deve_ser_BASE_URL_com_barra_no_final(self):
        r = self.view.get(self.request)
        r.render()
        dom = html.fromstring(r.content)
        esperado = u"%s/" % settings.BASE_URL
        self.assertEquals(esperado, dom.xpath('//meta[@property="og:url"]')[0].attrib["content"].encode("iso-8859-1"))

    def test_og_image_deve_ser_logomarca_padrao_do_evento(self):
        r = self.view.get(self.request)
        r.render()
        dom = html.fromstring(r.content)
        esperado = u"%simg/logo-devincachu-facebook.png" % settings.STATIC_URL
        self.assertEquals(esperado, dom.xpath('//meta[@property="og:image"]')[0].attrib["content"].encode("iso-8859-1"))

    def test_og_description_deve_trazer_descricao_do_evento(self):
        r = self.view.get(self.request)
        r.render()
        dom = html.fromstring(r.content)
        esperado = u"Maior evento de desenvolvimento de software do sul do Espírito Santo. Organizado com o objetivo de difundir técnicas e práticas de desenvolvimento de software, trazendo diversos temas"
        self.assertEquals(esperado, dom.xpath('//meta[@property="og:description"]')[0].attrib["content"].encode("iso-8859-1"))


class IndexViewSemDados(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        management.call_command("flush", interactive=False, verbosity=0)

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
