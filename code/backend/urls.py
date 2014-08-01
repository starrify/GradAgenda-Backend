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

    url(r'^addevent/$', 'backend.calendarr.views.addEvent'),
    url(r'^getevents/$', 'backend.calendarr.views.getEventsInRange'),
    url(r'^alterevent/$', 'backend.calendarr.views.alterEvent'),

    url(r'^searchforuser/$', 'backend.friend.views.searchForUser'),
    url(r'^sendfriendrequest/$', 'backend.friend.views.sendFriendRequest'),
    url(r'^getfriendrequest/$', 'backend.friend.views.getFriendRequest'),
    url(r'^acceptfriendrequest/$', 'backend.friend.views.acceptFriendRequest'),
    url(r'^rejectfriendrequest/$', 'backend.friend.views.rejectFriendRequest'),
    url(r'^getfriendlist/$', 'backend.friend.views.getFriendList'),
    url(r'^isfriend/$', 'backend.friend.views.isFriend'),
    url(r'^deletefriend/$', 'backend.friend.views.deleteFriend'),


)

