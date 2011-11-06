from django.conf.urls.defaults import include, patterns, url
from django.views.generic import base

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', base.TemplateView.as_view(template_name='base.html')),
)
