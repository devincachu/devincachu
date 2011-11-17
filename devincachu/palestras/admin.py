# -*- coding: utf-8 -*-
from django.contrib import admin
from django.template import defaultfilters as filters

from palestras import forms, models


class PalestranteAdmin(admin.ModelAdmin):
    form = forms.PalestranteAdminForm
    list_display = ('nome', 'slug')
    search_fields = ('nome',)

    def save_model(self, request, obj, form, change):
        obj.slug = filters.slugify(obj.nome)
        obj.save()


admin.site.register(models.Palestrante, PalestranteAdmin)
