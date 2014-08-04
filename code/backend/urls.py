from django.conf.urls import patterns, include, url
from backend import settings, views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'backend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^site_media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),

    url(r'^register/$', 'backend.personal.views.register'),
    url(r'^login/$', 'backend.personal.views.login'),
    url(r'^logout/$', 'backend.personal.views.logout'),
    url(r'^edit/$', 'backend.personal.views.edit'),
    url(r'^edit/password/$', 'backend.personal.views.editPw'),
    url(r'^fblogin/$', 'backend.personal.views.login_facebook'),
    url(r'^info/$', 'backend.personal.views.userInfo'),

)

