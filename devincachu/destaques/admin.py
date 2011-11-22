# -*- coding: utf-8 -*-
from django.contrib import admin

from destaques import forms, models


class DestaqueAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data',)
    list_filter = ('autor',)
    search_fields = ('titulo',)
    form = forms.DestaqueAdminForm

    def save_model(self, request, obj, form, change):
        obj.autor = request.user
        obj.save()


class ChamadaAdmin(DestaqueAdmin):
    list_display = ('titulo', 'data', 'url_link')
    form = forms.ChamadaAdminForm

admin.site.register(models.Destaque, DestaqueAdmin)
admin.site.register(models.Chamada, ChamadaAdmin)
