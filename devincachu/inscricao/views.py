# -*- coding: utf-8 -*-
import logging

import requests

from django import http
from django.conf import settings
from django.core import mail
from django.template import loader, response
from django.views.generic import base, detail

from inscricao import forms, models
from lxml import etree

logger = logging.getLogger('devincachu.inscricoes')


class MailerMixin(object):

    def enviar_email(self, assunto, corpo, destinatarios):
        mail.send_mail(assunto, corpo, "contato@devincachu.com.br", destinatarios, fail_silently=True)


class Inscricao(base.View, MailerMixin):
    templates = {
        u"fechadas": "inscricoes_fechadas.html",
        u"abertas": "inscricoes_abertas.html",
        u"encerradas": "inscricoes_encerradas.html",
    }

    def __init__(self, *args, **kwargs):
        super(Inscricao, self).__init__(*args, **kwargs)
        self._configuracao = None

    @property
    def configuracao(self):
        if not self._configuracao:
            self._configuracao = models.Configuracao.objects.get()

        return self._configuracao

    def get(self, request):
        contexto = self.obter_contexto(self.configuracao)
        return response.TemplateResponse(request, self.templates[self.configuracao.status], contexto)

    def obter_contexto(self, configuracao):
        status = configuracao.status
        nome_do_metodo = "obter_contexto_inscricoes_%s" % status
        metodo = getattr(self, nome_do_metodo, None)
        return metodo and metodo(configuracao) or {}

    def obter_contexto_inscricoes_abertas(self, configuracao):
        form = forms.ParticipanteForm()
        return {"form": form, "configuracao": configuracao}

    def enviar_email_sucesso(self, checkout):
        conteudo = loader.render_to_string("email_aguardando.html", {"checkout": checkout})
        assunto = u"[Dev in Cachu 2012] Inscrição recebida"
        self.enviar_email(assunto, conteudo, [checkout.participante.email])

    def enviar_email_falha(self, participante):
        conteudo = loader.render_to_string("email_falha.html", {"participante": participante})
        assunto = u"[Dev in Cachu 2012] Inscrição recebida"
        self.enviar_email(assunto, conteudo, [participante.email, "contato@devincachu.com.br"])

    def gerar_cobranca(self, participante):
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        payload = settings.PAGSEGURO
        payload["itemAmount1"] = "%.2f" % self.configuracao.valor_inscricao
        payload["reference"] = "%s" % participante.pk
        response = requests.post(settings.PAGSEGURO_CHECKOUT, data=payload, headers=headers)
        if response.ok:
            dom = etree.fromstring(response.content)
            codigo_checkout = dom.xpath("//code")[0].text
            return codigo_checkout
        else:
            logger.error("\n\n\n########## Erro na inscrição do participante %d - %s (%s) ##########" % (participante.pk, participante.nome, participante.email))
            logger.error("Erro na comunicação com PagSeguro: %s - %s" % (response.status_code, response.content))
            logger.error("#################################################################\n\n\n")
            return None

    def post(self, request):
        form = forms.ParticipanteForm(request.POST)
        if form.is_valid():
            participante = form.save()
            codigo_checkout = self.gerar_cobranca(participante)

            if codigo_checkout:
                checkout = models.Checkout.objects.create(codigo=codigo_checkout, participante=participante)
                self.enviar_email_sucesso(checkout)
                return response.TemplateResponse(request, "aguardando_pagamento.html", {"checkout": checkout})

            self.enviar_email_falha(participante)
            return response.TemplateResponse(request, "falha_comunicacao_pagseguro.html", {"participante": participante})

        contexto = {"form": form, "configuracao": self.configuracao}
        return response.TemplateResponse(request, "inscricoes_abertas.html", contexto)


class Notificacao(base.View, MailerMixin):

    def __init__(self, *args, **kwargs):
        super(Notificacao, self).__init__(*args, **kwargs)
        self.metodos_por_status = {
            3: self.inscricao_paga,
            7: self.inscricao_cancelada,
        }

    def enviar_email_confirmacao(self, participante):
        assunto = u"[Dev in Cachu 2012] Inscrição confirmada"
        conteudo = loader.render_to_string("inscricao_confirmada.html", {"participante": participante})
        destinatarios = [participante.email]
        self.enviar_email(assunto, conteudo, destinatarios)

    def inscricao_paga(self, referencia):
        participante = models.Participante.objects.get(pk=referencia)
        participante.status = u"CONFIRMADO"
        participante.save()

        self.enviar_email_confirmacao(participante)

    def enviar_email_cancelamento(self, participante):
        assunto = u"[Dev in Cachu 2012] Inscrição cancelada"
        conteudo = loader.render_to_string("inscricao_cancelada.html", {"participante": participante})
        destinatarios = [participante.email]
        self.enviar_email_cancelamento(assunto, conteudo, destinatarios)

    def inscricao_cancelada(self, referencia):
        participante = models.Participante.objects.get(pk=referencia)
        participante.status = u"CANCELADO"
        participante.save()
        self.enviar_email_cancelamento(participante)

    def consultar_transacao(self, codigo_transacao):
        url_transacao = "%s/%s?email=%s&token=%s" % (settings.PAGSEGURO_TRANSACTIONS, codigo_transacao, settings.PAGSEGURO["email"], settings.PAGSEGURO["token"])
        url_notificacao = "%s/%s?email=%s&token=%s" % (settings.PAGSEGURO_TRANSACTIONS_NOTIFICATIONS, codigo_transacao, settings.PAGSEGURO["email"], settings.PAGSEGURO["token"])

        response = requests.get(url_transacao)
        if not response.ok:
            response = requests.get(url_notificacao)

        if response.ok:
            dom = etree.fromstring(response.content)
            status_transacao = int(dom.xpath("//status")[0].text)
            referencia = int(dom.xpath("//reference")[0].text)

            return status_transacao, referencia

        logger.error(u"\n\n")
        logger.error(u"ERROR: Erro ao fazer requisição para o PagSeguro")
        logger.error(u"url requisitada (transação): %s" % url_transacao)
        logger.error(u"url requisitada (notificação): %s" % url_notificacao)
        logger.error(u"código da transação: %s" % codigo_transacao)
        logger.error(u"Response obtido: %s\n%s" % (response.status_code, response.content))
        logger.error(u"\n\n")

        return None, None

    def post(self, request):
        codigo_notificacao = request.POST.get("notificationCode")

        if codigo_notificacao:
            status, referencia = self.consultar_transacao(codigo_notificacao)
            metodo = self.metodos_por_status.get(status)

            if metodo:
                metodo(referencia)

        return http.HttpResponse("OK")


class Certificado(detail.DetailView):
    context_object_name = u"certificado"
    queryset = models.Certificado.objects.select_related("participante")
    slug_field = u"hash"
    template_name = u"certificado.html"


class ValidacaoCertificado(base.View):

    def get(self, request):
        form = forms.ValidacaoCertificado()
        return response.TemplateResponse(request, "form_validacao_certificado.html", {"form": form})

    def post(self, request):
        contexto = {}
        form = forms.ValidacaoCertificado(request.POST)
        cert = form.obter_certificado()
        if cert is None:
            contexto["msg"] = u"Código inválido, verifique o valor digitado"
            contexto["form"] = form
            template_name = "form_validacao_certificado.html"
        else:
            contexto["certificado"] = cert
            template_name = "certificado_valido.html"
        return response.TemplateResponse(request, template_name, contexto)
