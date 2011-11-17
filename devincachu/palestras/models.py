from django.db import models


class Palestrante(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    minicurriculo = models.CharField(max_length=500)
    blog = models.URLField(verify_exists=False, max_length=255, blank=True)
    twitter = models.CharField(max_length=50, blank=True)
    foto = models.ImageField(upload_to=u"palestrantes")
