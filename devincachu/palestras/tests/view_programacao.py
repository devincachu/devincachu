# -*- coding: utf-8 -*-
import unittest

from django.conf import settings
from django.core import management
from django.test import client
from django.views.generic import list as vlist
from lxml import html

from palestras import models, views


class ProgramacaoViewTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        management.call_command("loaddata", "palestrantes", "palestras", verbosity=0)

    @classmethod
    def tearDownClass(cls):
        management.call_command("flush", verbosity=0, interactive=False)

    def setUp(self):
        factory = client.RequestFactory()
        self.request = factory.get("/programacao")

    def test_deve_herdar_de_ListView(self):
        assert issubclass(views.ProgramacaoView, vlist.ListView)

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

    def test_nao_deve_incluir_tags_html_no_title_da_grade_de_programacao(self):
        palestra = models.Palestra.objects.get(pk=1)
        palestra.descricao = u"[Oi](http://www.google.com.br), você vem sempre aqui?"
        palestra.save()

        view = views.ProgramacaoView.as_view()
        response = view(self.request)
        response.render()

        dom = html.fromstring(response.content)
        title_obtido = dom.xpath('//a[@href="%s"]' % palestra.get_absolute_url())[0].attrib["title"].encode("iso-8859-1")
        self.assertEquals(u"Oi, você vem sempre aqui?", title_obtido)

    def test_deve_definir_canonical_url(self):
        esperado = "%s/programacao/" % settings.BASE_URL
        view = views.ProgramacaoView.as_view()
        response = view(self.request)
        response.render()
        dom = html.fromstring(response.content)
        self.assertEquals(esperado, dom.xpath('//link[@rel="canonical"]')[0].attrib["href"])

    def test_deve_ter_meta_keywords(self):
        esperado = u"devincachu, dev in cachu 2012, palestras, programação, desenvolvimento de software"
        view = views.ProgramacaoView.as_view()
        response = view(self.request)
        response.render()
        dom = html.fromstring(response.content)
        self.assertEquals(esperado, dom.xpath('//meta[@name="keywords"]')[0].attrib["content"].encode("iso-8859-1"))

    def test_deve_ter_meta_description(self):
        esperado = u"Grade de programação do Dev in Cachu 2012"
        view = views.ProgramacaoView.as_view()
        response = view(self.request)
        response.render()
        dom = html.fromstring(response.content)
        self.assertEquals(esperado, dom.xpath('//meta[@name="description"]')[0].attrib["content"].encode("iso-8859-1"))

    def test_deve_ter_og_description(self):
        esperado = u"Conheça as atrações e os convidados especiais do Dev in Cachu 2012"
        view = views.ProgramacaoView.as_view()
        response = view(self.request)
        response.render()
        dom = html.fromstring(response.content)
        self.assertEquals(esperado, dom.xpath('//meta[@property="og:description"]')[0].attrib["content"].encode("iso-8859-1"))

    def test_deve_ter_og_title_descrevendo_a_pagin(self):
        esperado = u"Grade de programação do Dev in Cachu 2012"
        view = views.ProgramacaoView.as_view()
        response = view(self.request)
        response.render()
        dom = html.fromstring(response.content)
        self.assertEquals(esperado, dom.xpath('//meta[@property="og:title"]')[0].attrib["content"].encode("iso-8859-1"))

    def test_deve_ter_og_type_activity(self):
        view = views.ProgramacaoView.as_view()
        response = view(self.request)
        response.render()
        dom = html.fromstring(response.content)
        self.assertEquals(u"activity", dom.xpath('//meta[@property="og:type"]')[0].attrib["content"].encode("iso-8859-1"))

    def test_deve_ter_og_url(self):
        esperado = "%s/programacao/" % settings.BASE_URL
        view = views.ProgramacaoView.as_view()
        response = view(self.request)
        response.render()
        dom = html.fromstring(response.content)
        self.assertEquals(esperado, dom.xpath('//meta[@property="og:url"]')[0].attrib["content"].encode("iso-8859-1"))

    def test_deve_ter_og_image_apontando_para_logo_do_devincachu(self):
        esperado = "%simg/logo-devincachu-facebook.png" % settings.STATIC_URL
        view = views.ProgramacaoView.as_view()
        response = view(self.request)
        response.render()
        dom = html.fromstring(response.content)
        self.assertEquals(esperado, dom.xpath('//meta[@property="og:image"]')[0].attrib["content"].encode("iso-8859-1"))
