from django.conf.urls import patterns, include, url
from gradagenda import settings, views
from register.views import show, register
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^site_media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    url(r'^register/$', register),
    url(r'^register/show/$', show),
    # Examples:
    # url(r'^$', 'gradagenda.views.home', name='home'),
    # url(r'^gradagenda/', include('gradagenda.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
