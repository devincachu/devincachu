# -*- coding: utf-8 -*-
from django.contrib import admin

from inscricao import models


class CheckoutAdmin(admin.ModelAdmin):
    list_display = (u"codigo", u"nome_participante", u"email_participante",)
    search_fields = (u"codigo", u"participante__nome", u"participante__email",)

    def has_add_permission(self, *args, **kwargs):
        return False

    def nome_participante(self, chk):
        return chk.participante.nome

    def email_participante(self, chk):
        return chk.participante.email


class ConfiguracaoAdmin(admin.ModelAdmin):

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False


class ParticipanteAdmin(admin.ModelAdmin):
    list_display = (u"nome", u"sexo", u"email", u"empresa", u"instituicao_ensino", u"tamanho_camiseta", u"status",)
    list_filter = (u"tamanho_camiseta", u"sexo", u"status",)
    search_fields = (u"nome", u"email",)

admin.site.register(models.Checkout, CheckoutAdmin)
admin.site.register(models.Configuracao, ConfiguracaoAdmin)
admin.site.register(models.Participante, ParticipanteAdmin)
