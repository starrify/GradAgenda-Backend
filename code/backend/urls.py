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

    url(r'^addevent/$', 'backend.calendarr.views.addEvent'),
    url(r'^geteventlist/$', 'backend.calendarr.views.getEventList'),
    url(r'^getevent/$', 'backend.calendarr.views.getEvent'),
    url(r'^alterevent/$', 'backend.calendarr.views.alterEvent'),
    url(r'^deleteevent/$', 'backend.calendarr.views.deleteEvent'),

    url(r'^searchforuser/$', 'backend.friend.views.searchForUser'),
    url(r'^sendfriendrequest/$', 'backend.friend.views.sendFriendRequest'),
    url(r'^getfriendrequest/$', 'backend.friend.views.getFriendRequest'),
    url(r'^acceptfriendrequest/$', 'backend.friend.views.acceptFriendRequest'),
    url(r'^rejectfriendrequest/$', 'backend.friend.views.rejectFriendRequest'),
    url(r'^getfriendlist/$', 'backend.friend.views.getFriendList'),
    url(r'^isfriend/$', 'backend.friend.views.isFriend'),
    url(r'^deletefriend/$', 'backend.friend.views.deleteFriend'),
    url(r'^getsamecourses/$', 'backend.friend.views.getSameCourses'),
    url(r'^getusersinfo/$', 'backend.friend.views.getUsersInfo'),
    url(r'^getsamecourseusers/$', 'backend.friend.views.getSameCourseUsers'),

    url(r'^inputunivinfo/$', 'backend.univinfo.views.inputUnivinfo'),
    url(r'^issupported/$', 'backend.univinfo.views.isSupported'),
    url(r'^getuniversities/$', 'backend.univinfo.views.getUniversities'),
    url(r'^getmajors/$', 'backend.univinfo.views.getMajors'),
    url(r'^getsemesters/$', 'backend.univinfo.views.getSemesters'),
    url(r'^getprofessors/$', 'backend.univinfo.views.getProfessors'),
    url(r'^getcourse/$', 'backend.univinfo.views.getCourse'),
    url(r'^getsection/$', 'backend.univinfo.views.getSection'),
    url(r'^getlectures/$', 'backend.univinfo.views.getLectures'),
    url(r'^getuniversitiesinfo/$', 'backend.univinfo.views.getUniversitiesInfo'),
    url(r'^getmajorsinfo/$', 'backend.univinfo.views.getMajorsInfo'),
    url(r'^getcoursesinfo/$', 'backend.univinfo.views.getCoursesInfo'),

    url(r'^fetchcurriculum/$', 'backend.curriculum.views.fetchCurriculum'),
    url(r'^getcourselist/$', 'backend.curriculum.views.getCourseList'),
    url(r'^setreview/$', 'backend.curriculum.views.setReview'),
    url(r'^deletereview/$', 'backend.curriculum.views.deleteReview'),


)

