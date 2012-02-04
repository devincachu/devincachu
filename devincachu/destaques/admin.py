# -*- coding: utf-8 -*-
from django.contrib import admin

from destaques import forms, models


class DestaqueAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data',)
    list_filter = ('autor',)
    search_fields = ('titulo',)
    form = forms.DestaqueAdminForm

    def save_model(self, request, obj, form, change):
        if not change:
            obj.autor = request.user
            obj.save()

    def queryset(self, request):
        qs = super(DestaqueAdmin, self).queryset(request)
        return qs.filter(chamada__isnull=True)


class ChamadaAdmin(DestaqueAdmin):
    list_display = ('titulo', 'data', 'url_link')
    form = forms.ChamadaAdminForm

    def queryset(self, request):
        return admin.ModelAdmin.queryset(self, request)

admin.site.register(models.Destaque, DestaqueAdmin)
admin.site.register(models.Chamada, ChamadaAdmin)
