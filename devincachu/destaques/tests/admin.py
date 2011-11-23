# -*- coding: utf-8 -*-
import unittest

from django.contrib import admin as django_admin
from django.contrib.auth import models as auth_models
from django.test import client

from destaques import admin, forms, models


class DestaqueAdminTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user, created = auth_models.User.objects.get_or_create(username='devincachu', email='contato@devincachu.com.br')
        if created:
            cls.user.set_password('123')
            cls.user.save()

        cls.destaque_persistido = models.Destaque.objects.create(titulo=u"Dev in Cachu 2012", conteudo=u"Se inscreva!", autor=cls.user)
        cls.chamada_persistida = models.Chamada.objects.create(titulo=u"Inscrições abertas", conteudo=u"Bla", autor=cls.user, url_link="/inscricao/", titulo_veja_mais=u"Se inscreva agora!")

    @classmethod
    def tearDownClass(cls):
        cls.destaque_persistido.delete()
        cls.chamada_persistida.delete()

    def setUp(self):
        self.factory = client.RequestFactory()
        self.request = self.factory.get("/")
        self.request.user = self.user
        self.destaque = models.Destaque(titulo=u"Começou o Dev in Cachu 2012", conteudo=u"Faça parte!")

        self.admin = admin.DestaqueAdmin(self.destaque, None)

    def test_model_destaque_deve_estar_registrado_no_admin(self):
        self.assertIn(models.Destaque, django_admin.site._registry)

    def test_model_destaque_deve_estar_registrado_com_a_classe_DestaQueAdmin(self):
        self.assertIsInstance(django_admin.site._registry[models.Destaque], admin.DestaqueAdmin)

    def test_DestaqueAdmin_deve_usar_DestaqueAdminForm(self):
        self.assertEquals(forms.DestaqueAdminForm, admin.DestaqueAdmin.form)

    def test_titulo_deve_estar_na_listagem(self):
        self.assertIn('titulo', admin.DestaqueAdmin.list_display)

    def test_data_deve_estar_na_listagem(self):
        self.assertIn('data', admin.DestaqueAdmin.list_display)

    def test_autor_deve_estar_na_filtragem(self):
        self.assertIn('autor', admin.DestaqueAdmin.list_filter)

    def test_deve_ser_possivel_buscar_pelo_titulo(self):
        self.assertIn('titulo', admin.DestaqueAdmin.search_fields)

    def test_deve_gravar_usuario_logado_como_autor_de_destaque(self):
        self.admin.save_model(self.request, self.destaque, None, None)
        self.assertEquals(self.user, self.destaque.autor)

    def test_deve_excluir_chamadas_da_listagem(self):
        qs = self.admin.queryset(self.request)
        self.assertEquals(self.destaque_persistido, qs.get())


class ChamadaAdminTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user, created = auth_models.User.objects.get_or_create(username='devincachu', email='contato@devincachu.com.br')
        if created:
            cls.user.set_password('123')
            cls.user.save()

        cls.destaque_persistido = models.Destaque.objects.create(titulo=u"Dev in Cachu 2012", conteudo=u"Se inscreva!", autor=cls.user)
        cls.chamada_persistida = models.Chamada.objects.create(titulo=u"Inscrições abertas", conteudo=u"Bla", autor=cls.user, url_link="/inscricao/", titulo_veja_mais=u"Se inscreva agora!")

    @classmethod
    def tearDownClass(cls):
        cls.destaque_persistido.delete()
        cls.chamada_persistida.delete()

    def setUp(self):
        self.factory = client.RequestFactory()
        self.request = self.factory.get("/")
        self.request.user = self.user

        self.admin = admin.ChamadaAdmin(self.chamada_persistida, None)

    def test_model_Chamada_deve_estar_registro_no_admin(self):
        self.assertIn(models.Chamada, django_admin.site._registry)

    def test_model_chamada_deve_estar_registrado_com_a_classe_ChamadaAdmin(self):
        self.assertIsInstance(django_admin.site._registry[models.Chamada], admin.ChamadaAdmin)

    def test_ChamadaAdmin_deve_herdar_de_DestaqueAdmin(self):
        assert issubclass(admin.ChamadaAdmin, admin.DestaqueAdmin)

    def test_ChamadaAdmin_deve_usar_ChamadaAdminForm(self):
        self.assertEquals(forms.ChamadaAdminForm, admin.ChamadaAdmin.form)

    def test_titulo_deve_permarnecer_na_listagem(self):
        self.assertIn('titulo', admin.ChamadaAdmin.list_display)

    def test_data_deve_permernecer_na_listagem(self):
        self.assertIn('data', admin.ChamadaAdmin.list_display)

    def test_link_deve_estar_na_listagem(self):
        self.assertIn('url_link', admin.ChamadaAdmin.list_display)

    def test_deve_trazer_apenas_chamada_na_listagem(self):
        qs = self.admin.queryset(self.request)
        self.assertEquals(self.chamada_persistida, qs.get())
