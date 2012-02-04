# -*- coding: utf-8 -*-
from django.contrib import admin

from inscricao import models


class ConfiguracaoAdmin(admin.ModelAdmin):

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False


class ParticipanteAdmin(admin.ModelAdmin):
    list_display = (u"nome", u"sexo", u"email", u"empresa", u"instituicao_ensino", u"tamanho_camiseta", u"confirmado",)
    list_filter = (u"tamanho_camiseta", u"sexo", u"confirmado",)
    search_fields = (u"nome", u"email",)

admin.site.register(models.Configuracao, ConfiguracaoAdmin)
admin.site.register(models.Participante, ParticipanteAdmin)
