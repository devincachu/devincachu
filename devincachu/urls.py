from django.conf import settings
from django.conf.urls.defaults import include, patterns, url

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
    url(r'^notificacao/$', iviews.Notificacao.as_view(), name='notificacao'),
    url(r'^$', dviews.IndexView.as_view(), name='index'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
