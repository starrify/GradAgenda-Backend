from django.conf.urls import patterns, include, url

from backend import settings, views
from backend.personal.views import register, login, edit

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'backend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^site_media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    url(r'^register/$', register),
    url(r'^login/$', login),
    url(r'^edit/$', edit),
)

