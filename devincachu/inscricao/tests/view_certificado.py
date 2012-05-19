# -*- coding: utf-8 -*-
from django import test
from django.core import management
from django.views.generic import base, detail
from django.template import response
from django.test import client

from inscricao import forms, views


class ViewCertificadoTestCase(test.TestCase):

    @classmethod
    def setUpClass(cls):
        management.call_command("loaddata", "certificados.yaml", verbosity=0)

    @classmethod
    def tearDownClass(cls):
        management.call_command("flush", interactive=False, verbosity=0)

    def test_view_deve_herdar_de_DetailView(self):
        assert issubclass(views.Certificado, detail.DetailView)

    def test_template_name_deve_ser_certificado_html(self):
        self.assertEqual(u"certificado.html", views.Certificado.template_name)

    def test_slug_field_deve_ser_hash(self):
        self.assertEqual(u"hash", views.Certificado.slug_field)

    def test_context_object_name_deve_ser_certificado(self):
        self.assertEqual(u"certificado", views.Certificado.context_object_name)

    def test_queryset_deve_fazer_uma_query_so_para_obter_informacao_de_participante(self):
        with self.assertNumQueries(1):
            v = views.Certificado()
            self.assertEqual("Joaozinho", v.queryset[0].participante.nome)


class ValidacaoCertificado(test.TestCase):

    @classmethod
    def setUpClass(cls):
        management.call_command("loaddata", "certificados.yaml", verbosity=0)
        cls.factory = client.RequestFactory()

    @classmethod
    def tearDownClass(cls):
        management.call_command("flush", interactive=False, verbosity=0)

    def test_deve_herdar_de_view(self):
        assert issubclass(views.ValidacaoCertificado, base.View)

    def test_metodo_get_deve_retornar_template_response(self):
        request = self.factory.get("/certificado/validar")
        v = views.ValidacaoCertificado()
        r = v.get(request)
        self.assertIsInstance(r, response.TemplateResponse)

    def test_metodo_get_deve_renderizar_template_form_validacao_certificado(self):
        request = self.factory.get("/certificado/validar")
        v = views.ValidacaoCertificado()
        r = v.get(request)
        self.assertEqual("form_validacao_certificado.html", r.template_name)

    def test_metodo_get_deve_incluir_instancia_do_formulario_no_contexto(self):
        request = self.factory.get("/certificado/validar")
        v = views.ValidacaoCertificado()
        r = v.get(request)
        form = r.context_data["form"]
        self.assertIsInstance(form, forms.ValidacaoCertificado)
