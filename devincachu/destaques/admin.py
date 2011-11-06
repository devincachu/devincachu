# -*- coding: utf-8 -*-
from django.contrib import admin

from destaques import forms, models


class DestaqueAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data',)
    list_filter = ('autor',)
    search_fields = ('titulo',)
    form = forms.DestaqueAdminForm

admin.site.register(models.Destaque, DestaqueAdmin)
