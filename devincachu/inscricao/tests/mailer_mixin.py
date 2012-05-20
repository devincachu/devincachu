# -*- coding: utf-8 -*-
import unittest

from django.core import mail

from inscricao import views


class MailerMixinTestCase(unittest.TestCase):

    def setUp(self):
        mail.outbox = []

    def test_enviar_email_deve_enviar_email_com_parametros_passados(self):
        mailer = views.MailerMixin()
        mailer.enviar_email(u"Assunto", u"Corpo", ["eu@gmail.com"])
        email = mail.outbox[0]
        self.assertEqual(u"Assunto", email.subject)
        self.assertEqual(u"Corpo", email.body)
        self.assertEqual(["eu@gmail.com"], email.to)

    def test_enviar_email_deve_enviar_email_como_contato_at_devincachu(self):
        mailer = views.MailerMixin()
        mailer.enviar_email(u"Assunto", u"Corpo", ["eu@gmail.com"])
        email = mail.outbox[0]
        self.assertEqual("contato@devincachu.com.br", email.from_email)
