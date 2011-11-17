# -*- coding: utf-8 -*-
import unittest

from django.views.generic import list

from palestras import models, views


class PalestrantesViewTestCase(unittest.TestCase):

    def test_deve_herdar_de_ListView(self):
        assert issubclass(views.PalestrantesView, list.ListView)

    def test_template_name_deve_ser_palestrantes(self):
        self.assertEquals("palestrantes.html", views.PalestrantesView.template_name)

    def test_model_deve_ser_Palestrante(self):
        self.assertEquals(models.Palestrante, views.PalestrantesView.model)

    def test_context_object_name_deve_ser_palestrantes(self):
        self.assertEquals("palestrantes", views.PalestrantesView.context_object_name)
