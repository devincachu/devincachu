# -*- coding: utf-8 -*-
from django import test
from django.core import management, urlresolvers as u
from django.test import client
from django.views.generic import list
from lxml import html

from palestras import models, views


class PalestrantesViewTestCase(test.TestCase):

    def test_deve_herdar_de_ListView(self):
        assert issubclass(views.PalestrantesView, list.ListView)

    def test_template_name_deve_ser_palestrantes(self):
        self.assertEquals("palestrantes.html", views.PalestrantesView.template_name)

    def test_model_deve_ser_Palestrante(self):
        self.assertEquals(models.Palestrante, views.PalestrantesView.model)

    def test_context_object_name_deve_ser_palestrantes(self):
        self.assertEquals("palestrantes", views.PalestrantesView.context_object_name)

    def test_deve_estar_mapeado_para_url_palestrantes(self):
        f = views.PalestrantesView.as_view()
        resolve = u.resolve("/palestrantes/")
        self.assertEquals(f.func_code, resolve.func.func_code)


class TemplatePalestrantesTestCase(test.TestCase):

    @classmethod
    def setUpClass(cls):
        management.call_command("loaddata", "palestrantes.yaml", verbosity=0)

    @classmethod
    def tearDownClass(cls):
        management.call_command("flush", verbosity=0, interactive=False)

    def setUp(self):
        factory = client.RequestFactory()
        request = factory.get("/palestrantes")
        view = views.PalestrantesView.as_view()
        self.response = view(request)
        self.response.render()
        self.dom = html.fromstring(self.response.content)

    def test_deve_trazer_listagem_de_palestrantes_em_ul_com_class_palestrante(self):
        lis = self.dom.xpath('//ul[@class="palestrantes"]/li')
        self.assertEquals(5, len(lis))

    def test_deve_identificar_de_forma_unica_lis_impares_comecando_em_0(self):
        lis = self.dom.xpath('//ul[@class="palestrantes"]/li')
        for i, li in enumerate(lis):
            if i % 2 == 1:
                self.assertIn("impar", li.attrib['class'])

    def test_deve_trazer_palestrantes_em_ordem_alfabetica(self):
        lista_esperada = ["Forrest Gump", "Freddy Krueger", "Hannibal Lecter", "James Bond", "Vito Corleone"]
        lista_obtida = [p.nome for p in self.response.context_data["palestrantes"]]
        self.assertEquals(lista_esperada, lista_obtida)

    def test_deve_trazer_link_para_o_blog_caso_o_palestrante_tenha_blog(self):
        link = self.dom.xpath('//ul[@class="palestrantes"]/li/div/a[@href="http://bond.com"]')
        self.assertEquals(1, len(link))

    def test_nao_deve_trazer_link_para_o_blog_caso_o_palestrante_nao_tenha_blog(self):
        divs = self.dom.xpath('//ul[@class="palestrantes"]/li/div')
        div = divs[4]
        children = div.getchildren()
        c = 0
        for child in children:
            if child.tag == 'a':
                c += 1

        self.assertEquals(1, c)

    def test_deve_ter_link_para_twitter_caso_o_palestrante_tenha_twitter(self):
        link = self.dom.xpath('//ul[@class="palestrantes"]/li/div/a[@href="http://twitter.com/hlecter"]')
        self.assertEquals(1, len(link))

    def test_deve_ter_link_para_twitter_correto_caso_o_palestrante_tenha_twitter_comecando_em_arroba(self):
        link = self.dom.xpath('//ul[@class="palestrantes"]/li/div/a[@href="http://twitter.com/vito"]')
        self.assertEquals(1, len(link))


class TemplatePalestranteSemPalestrantesTestCase(test.TestCase):

    def setUp(self):
        factory = client.RequestFactory()
        request = factory.get("/palestrantes")
        view = views.PalestrantesView.as_view()
        self.response = view(request)
        self.response.render()
        self.dom = html.fromstring(self.response.content)

    def test_nao_deve_renderizar_ul(self):
        ul = self.dom.xpath('//ul[@class="palestrantes"]')
        self.assertEquals(0, len(ul))

    def test_deve_exibir_mensagem_que_nao_ha_palestrantes(self):
        msg = "Não há palestrantes ainda :( Envie sua ideia para contato@devincachu.com.br!"
        self.assertIn(msg, self.response.content)
