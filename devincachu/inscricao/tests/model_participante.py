# -*- coding: utf-8 -*-
import unittest

from django.db import models as django_models

from inscricao import models


class ParticipanteTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.field_names = models.Participante._meta.get_all_field_names()

    def test_deve_ter_campo_com_o_nome_do_participante(self):
        self.assertIn("nome", self.field_names)

    def test_nome_deve_ser_do_tipo_CharField(self):
        field = models.Participante._meta.get_field_by_name("nome")[0]
        self.assertIsInstance(field, django_models.CharField)

    def test_nome_deve_ter_no_maximo_100_caracteres(self):
        field = models.Participante._meta.get_field_by_name("nome")[0]
        self.assertEquals(100, field.max_length)

    def test_deve_ter_campo_nome_no_cracha(self):
        self.assertIn("nome_cracha", self.field_names)

    def test_nome_no_cracha_deve_ser_do_tipo_CharField(self):
        field = models.Participante._meta.get_field_by_name("nome_cracha")[0]
        self.assertIsInstance(field, django_models.CharField)

    def test_nome_no_cracha_deve_ter_no_maximo_100_caracteres(self):
        field = models.Participante._meta.get_field_by_name("nome_cracha")[0]
        self.assertEquals(100, field.max_length)

    def test_nome_no_cracha_nao_deve_ser_obrigatorio(self):
        field = models.Participante._meta.get_field_by_name("nome_cracha")[0]
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_nome_no_cracha_deve_ter_verbose_name_com_acento(self):
        field = models.Participante._meta.get_field_by_name("nome_cracha")[0]
        self.assertEquals(u"Nome no crachá", field.verbose_name)

    def test_deve_ter_campo_sexo(self):
        self.assertIn("sexo", self.field_names)

    def test_campo_sexo_deve_ser_do_tipo_CharField(self):
        field = models.Participante._meta.get_field_by_name("sexo")[0]
        self.assertIsInstance(field, django_models.CharField)

    def test_campo_sexo_deve_ter_no_maximo_1_caracter(self):
        field = models.Participante._meta.get_field_by_name("sexo")[0]
        self.assertEquals(1, field.max_length)

    def test_campo_sexo_deve_ter_m_ou_f(self):
        esperado = (
            (u"M", u"Masculino"),
            (u"F", u"Feminino"),
        )
        field = models.Participante._meta.get_field_by_name("sexo")[0]
        self.assertEquals(esperado, field.choices)

    def test_deve_ter_campo_email(self):
        self.assertIn("email", self.field_names)

    def test_email_deve_ser_do_tipo_EmailField(self):
        field = models.Participante._meta.get_field_by_name("email")[0]
        self.assertIsInstance(field, django_models.EmailField)

    def test_email_deve_ter_no_maximo_100_caracteres(self):
        field = models.Participante._meta.get_field_by_name("email")[0]
        self.assertEquals(100, field.max_length)

    def test_email_e_status_devem_ser_unique_juntos(self):
        self.assertEquals((u'email', u'status',), models.Participante._meta.unique_together[0])

    def test_deve_ter_campo_status(self):
        self.assertIn("status", self.field_names)

    def test_campo_status_deve_ser_do_tipo_CharField(self):
        field = models.Participante._meta.get_field_by_name("status")[0]
        self.assertIsInstance(field, django_models.CharField)

    def test_campo_status_deve_ter_no_maximo_20_caracteres(self):
        field = models.Participante._meta.get_field_by_name("status")[0]
        self.assertEquals(20, field.max_length)

    def test_campo_stauts_deve_ser_AGUARDANDO_por_padrao(self):
        field = models.Participante._meta.get_field_by_name("status")[0]
        self.assertEquals(u"AGUARDANDO", field.default)

    def test_campo_status_deve_ter_choices_adequados(self):
        esperado = (
            (u'AGUARDANDO', u'Aguardando pagamento'),
            (u'CONFIRMADO', u'Confirmado'),
            (u'CANCELADO', u'Cancelado'),
        )

        field = models.Participante._meta.get_field_by_name("status")[0]
        self.assertEquals(esperado, field.choices)

    def test_deve_ter_campo_para_tamanho_de_camiseta(self):
        self.assertIn("tamanho_camiseta", self.field_names)

    def test_tamanho_de_camiseta_deve_ser_CharField(self):
        field = models.Participante._meta.get_field_by_name("tamanho_camiseta")[0]
        self.assertIsInstance(field, django_models.CharField)

    def test_tamanho_de_camiseta_deve_ter_no_maximo_2_caracteres(self):
        field = models.Participante._meta.get_field_by_name("tamanho_camiseta")[0]
        self.assertEquals(2, field.max_length)

    def test_tamanho_de_camiseta_deve_ter_verbose_name_descritivo(self):
        field = models.Participante._meta.get_field_by_name("tamanho_camiseta")[0]
        self.assertEquals(u"Tamanho da camiseta", field.verbose_name)

    def test_tamanho_de_camiseta_deve_ter_options_limitadas(self):
        esperado = (
            (u'P', u'P'),
            (u'M', u'M'),
            (u'G', u'G'),
            (u'GG', u'GG'),
        )
        field = models.Participante._meta.get_field_by_name("tamanho_camiseta")[0]
        self.assertEquals(esperado, field.choices)

    def test_deve_ter_instituicao_de_ensino(self):
        self.assertIn("instituicao_ensino", self.field_names)

    def test_instituicao_de_ensino_deve_ser_do_tipo_CharField(self):
        field = models.Participante._meta.get_field_by_name("instituicao_ensino")[0]
        self.assertIsInstance(field, django_models.CharField)

    def test_instituicao_de_ensino_deve_ter_no_maximo_100_caracteres(self):
        field = models.Participante._meta.get_field_by_name("instituicao_ensino")[0]
        self.assertEquals(100, field.max_length)

    def test_instituicao_de_ensino_nao_deve_ser_obrigatorio(self):
        field = models.Participante._meta.get_field_by_name("instituicao_ensino")[0]
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_instituicao_de_ensino_deve_ter_verbose_name_explicitando_que_eh_um_campo_para_estudantes(self):
        field = models.Participante._meta.get_field_by_name("instituicao_ensino")[0]
        self.assertEquals(u"Instituição de ensino (para estudantes)", field.verbose_name)

    def test_deve_ter_empresa(self):
        self.assertIn("empresa", self.field_names)

    def test_empresa_deve_ser_do_tipo_CharField(self):
        field = models.Participante._meta.get_field_by_name("empresa")[0]
        self.assertIsInstance(field, django_models.CharField)

    def test_empresa_deve_ter_no_maximo_100_caracteres(self):
        field = models.Participante._meta.get_field_by_name("empresa")[0]
        self.assertEquals(100, field.max_length)

    def test_empresa_nao_deve_ser_obrigatorio(self):
        field = models.Participante._meta.get_field_by_name("empresa")[0]
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_empresa_deve_ter_verbose_name_explicitando_que_eh_um_campo_para_pessoas_que_trabalham(self):
        field = models.Participante._meta.get_field_by_name("empresa")[0]
        self.assertEquals(u"Empresa onde trabalha", field.verbose_name)

    def test__repr__deve_ter_nome(self):
        participante = models.Participante(nome=u"Francisco Souza")
        self.assertEquals(u"<Participante: Francisco Souza>", repr(participante))

    def test__unicode__deve_ser_o_nome(self):
        participante = models.Participante(nome=u"Francisco Souza")
        self.assertEquals(u"Francisco Souza", unicode(participante))
