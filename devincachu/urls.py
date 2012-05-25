from django.conf import settings
from django.conf.urls.defaults import include, patterns, url
from django.views.decorators import csrf

from django.contrib import admin
admin.autodiscover()

from destaques import views as dviews
from inscricao import views as iviews
from palestras import views as pviews

from purger import connect
connect()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^palestrantes/$', pviews.PalestrantesView.as_view(), name='palestrantes'),
    url(r'^programacao/$', pviews.ProgramacaoView.as_view(), name='programacao'),
    url(r'^programacao/(?P<palestrantes>.*)/(?P<slug>[\w-]+)/$', pviews.PalestraView.as_view(), name='palestra'),
    url(r'^inscricao/$', iviews.Inscricao.as_view(), name='inscricao'),
    url(r'^notificacao/$', csrf.csrf_exempt(iviews.Notificacao.as_view()), name='notificacao'),
    url(r'^certificado/validar/$', iviews.ValidacaoCertificado.as_view(), name='validacao_certificado'),
    url(r'^certificado/$', iviews.BuscarCertificado.as_view(), name='busca_certificado'),
    url(r'^certificado/(?P<slug>[0-9a-f]+)/$', iviews.Certificado.as_view(), name='certificado'),
    url(r'^$', dviews.IndexView.as_view(), name='index'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
