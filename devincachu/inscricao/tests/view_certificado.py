# -*- coding: utf-8 -*-
from django import http, test
from django.core import management
from django.views.generic import base, detail
from django.template import response
from django.test import client

from inscricao import forms, models, views


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

    def test_deve_ficar_no_cache_por_1_ano(self):
        certificado = models.Certificado.objects.get(pk=1)
        factory = client.RequestFactory()
        request = factory.get("/certificado/%s/" % certificado.hash)
        v = views.Certificado()
        resp = v.dispatch(request, slug=certificado.hash)
        self.assertEqual("max-age=31536000", resp["Cache-Control"])


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

    def test_metodo_get_deve_renderizar_template_form_validacao_certificado(self):
        request = self.factory.get("/certificado/validar")
        v = views.ValidacaoCertificado()
        r = v.get(request)
        self.assertIsInstance(r, response.TemplateResponse)
        self.assertEqual("form_validacao_certificado.html", r.template_name)

    def test_metodo_get_deve_incluir_instancia_do_formulario_no_contexto(self):
        request = self.factory.get("/certificado/validar")
        v = views.ValidacaoCertificado()
        r = v.get(request)
        form = r.context_data["form"]
        self.assertIsInstance(form, forms.ValidacaoCertificado)

    def test_metodo_post_deve_renderizar_template_certificado_valido_se_o_codigo_estiver_correto(self):
        request = self.factory.post("/certificado/validar", {"codigo": "2012080439"})
        v = views.ValidacaoCertificado()
        r = v.post(request)
        self.assertIsInstance(r, response.TemplateResponse)
        self.assertEqual("certificado_valido.html", r.template_name)

    def test_metodo_post_deve_trazer_certificado_no_contexto_da_resposta_se_o_codigo_estiver_correto(self):
        request = self.factory.post("/certificado/validar", {"codigo": "2012080439"})
        v = views.ValidacaoCertificado()
        r = v.post(request)
        esperado = models.Certificado.objects.all()[0]
        obtido = r.context_data["certificado"]
        self.assertEqual(esperado, obtido)

    def test_post_renderiza_o_template_de_formulario_com_mensagem_caso_nao_seja_possivel_encontrar_certificado(self):
        inputs = ({}, {"codigo": ""}, {"codigo": "123ble"})
        for input in inputs:
            request = self.factory.post("/certificado/validar", input)
            v = views.ValidacaoCertificado()
            r = v.post(request)
            self.assertEqual("form_validacao_certificado.html", r.template_name)
            form = r.context_data["form"]
            self.assertIsInstance(form, forms.ValidacaoCertificado)
            msg = r.context_data["msg"]
            self.assertEqual(u"Código inválido, verifique o valor digitado", msg)


class BuscarCertificadoViewTestCase(test.TestCase):

    @classmethod
    def setUpClass(cls):
        management.call_command("loaddata", "certificados.yaml", verbosity=0)
        cls.factory = test.RequestFactory()

    @classmethod
    def tearDownClass(cls):
        management.call_command("flush", interactive=False, verbosity=0)

    def test_deve_herdar_de_base_view(self):
        assert issubclass(views.BuscarCertificado, base.View)

    def test_deve_retornar_template_response_no_metodo_get(self):
        request = self.factory.get("/certificado/")
        view = views.BuscarCertificado()
        resp = view.get(request)
        self.assertIsInstance(resp, response.TemplateResponse)

    def test_deve_renderizar_template_de_formulario_de_busca_de_certificado(self):
        request = self.factory.get("/certificado/")
        view = views.BuscarCertificado()
        resp = view.get(request)
        self.assertEqual("form_busca_certificado.html", resp.template_name)

    def test_deve_incluir_uma_instancia_do_formulario_no_context(self):
        request = self.factory.get("/certificado/")
        view = views.BuscarCertificado()
        resp = view.get(request)
        self.assertIsInstance(resp.context_data["form"], forms.BuscarCertificado)

    def test_post_deve_redirecionar_para_pagina_do_certificado(self):
        certificado = models.Certificado.objects.get(pk=1)
        request = self.factory.post("/certificado/", {"email": "joaozinho@devincachu.com.br"})
        view = views.BuscarCertificado()
        resp = view.post(request)
        self.assertIsInstance(resp, http.HttpResponseRedirect)
        self.assertEqual("/certificado/%s/" % certificado.hash, resp["Location"])

    def test_post_deve_criar_certificado_no_banco_de_dados_caso_nao_exista_e_redirecionar_para_o_mesmo(self):
        request = self.factory.post("/certificado/", {"email": "pedrinho@devincachu.com.br"})
        view = views.BuscarCertificado()
        resp = view.post(request)
        self.assertIsInstance(resp, http.HttpResponseRedirect)
        certificado = models.Certificado.objects.get(participante__email="pedrinho@devincachu.com.br")
        self.assertEqual("/certificado/%s/" % certificado.hash, resp["Location"])

    def test_post_deve_retornar_pagina_com_formulario_caso_email_nao_seja_de_participante_presente_com_mensagem(self):
        request = self.factory.post("/certificado/", {"email": "mariazinha@devincachu.com.br"})
        view = views.BuscarCertificado()
        resp = view.post(request)
        self.assertIsInstance(resp, response.TemplateResponse)
        self.assertEqual("form_busca_certificado.html", resp.template_name)
        msg = u"E-mail não encontrado. Certifique-se de que você digitou o e-mail corretamente. Caso você considere essa mensagem incorreta, por favor entre em contato conosco"
        self.assertEqual(msg, resp.context_data["msg"])

    def test_post_deve_retornar_pagina_com_formulario_caso_email_nao_esteja_inscrito(self):
        request = self.factory.post("/certificado/", {"email": "patricinha@devincachu.com.br"})
        view = views.BuscarCertificado()
        resp = view.post(request)
        self.assertIsInstance(resp, response.TemplateResponse)
        self.assertEqual("form_busca_certificado.html", resp.template_name)
        msg = u"E-mail não encontrado. Certifique-se de que você digitou o e-mail corretamente. Caso você considere essa mensagem incorreta, por favor entre em contato conosco"
        self.assertEqual(msg, resp.context_data["msg"])

    def test_post_deve_retornar_pagina_com_formulario_caso_formulario_nao_seja_valido(self):
        request = self.factory.post("/certificado/", {"email": ""})
        view = views.BuscarCertificado()
        resp = view.post(request)
        self.assertIsInstance(resp, response.TemplateResponse)
        self.assertEqual("form_busca_certificado.html", resp.template_name)
        msg = u"O campo e-mail é obrigatório e deve ser um e-mail válido."
        self.assertEqual(msg, resp.context_data["msg"])
