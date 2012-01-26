# -*- coding: utf-8 -*-
import unittest

from django.core import management
from django.test import client
from django.views.generic import detail, list as vlist

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


class PalestraViewTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        management.call_command("loaddata", "palestrantes", "palestras", verbosity=0)

    @classmethod
    def tearDownClass(cls):
        management.call_command("flush", verbosity=0, interactive=False)

    def setUp(self):
        factory = client.RequestFactory()
        self.request = factory.get("/programacao/francisco-souza/django")

    def test_deve_herdar_de_DetailView(self):
        assert issubclass(views.PalestraView, detail.DetailView)

    def test_model_deve_ser_Palestra(self):
        self.assertEquals(models.Palestra, views.PalestraView.model)

    def test_context_object_name_deve_ser_palestra(self):
        self.assertEquals("palestra", views.PalestraView.context_object_name)

    def test_deve_renderizar_template_palestra_html(self):
        self.assertEquals("palestra.html", views.PalestraView.template_name)

    def test_deve_buscar_palestra_pelo_slug_informado(self):
        palestra = models.Palestra.objects.get(pk=3)
        view = views.PalestraView()
        view.kwargs = {u"slug": palestra.slug, u"palestrantes": "james-bond"}
        self.assertEquals(palestra, view.get_queryset()[0])

    def test_deve_verificar_se_os_palestrantes_passados_realmente_sao_os_palestrantes_da_palestra(self):
        palestra = models.Palestra.objects.get(pk=1)
        view = views.PalestraView()
        view.kwargs = {u"slug": palestra.slug, u"palestrantes": "chico-buarque"}
        self.assertEquals([], list(view.get_queryset()))

    def test_deve_retornar_apenas_uma_palestra_quando_tem_dois_palestrantes(self):
        palestra = models.Palestra.objects.get(pk=1)
        view = views.PalestraView()
        view.kwargs = {u"slug": palestra.slug, u"palestrantes": "hannibal-lecter/vito-corleone"}
        self.assertEquals(1, view.get_queryset().count())
