from django.urls import path, re_path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('',views.user, name='user'),
    path('mainmenu/', views.mainmenu, name='mainmenu'),
    path('mcmain/', views.mcmain, name='mcmain'),
    path('scmission/', views.scmission, name='scmission'),
    # path('mission/', views.mission, name='mission'),
    path('archive/', views.archive, name='archive'),
    path('sendmessage/', views.sendmessage, name='sendmessage'),
    path('nomissions/', views.nomissions, name='nomissions'),
    path('convertToJSON/', views.convertToJSON, name='convertToJSON'),
    path('searchByMissionID/', views.searchByMissionID, name='searchByMissionID'),
    #path('stt/', views.stt, name='stt'),
    re_path(r'^scmission/(?P<missionID>-?[0-9]+)$', views.scmissionID, name='scmissionID'),
    re_path(r'^deployment/(?P<missionID>[0-9]+)$', views.deployment, name='deployment'),
    re_path(r'^archiveDetail/(?P<missionID>[0-9]+)$', views.archiveDetail, name='archiveDetail'),
    re_path(r'^missionDetail/(?P<missionID>[0-9]+)$', views.missionDetail, name='missionDetail'),
    re_path(r'^updateStatus/(?P<missionID>[0-9]+)/(?P<status>\w+)$', views.updateStatus, name='updateStatus'),
    re_path(r'^missions/$', views.MissionList.as_view()),
    re_path(r'^missions/(?P<pk>[0-9]+)/$', views.MissionDetail.as_view()),
    re_path(r'^messagelogs/$', views.MessageLogList.as_view()),
    re_path(r'^messagelogs/(?P<pk>[0-9]+)/$', views.MessageLogDetail.as_view()),
    re_path(r'^plans/$', views.PlanList.as_view()),
    re_path(r'^plans/(?P<pk>[0-9]+)/$', views.PlanDetail.as_view()),
    re_path(r'^updates/$', views.UpdateList.as_view()),
    re_path(r'^updates/new/(?P<pk>[0-9]+)/$', views.UpdateNew.as_view()),
    # re_path(r'^updates/new/(?P<pk>[0-9]+)/$', views.UpdatePull),
    re_path(r'^test/new/(?P<pk>[0-9]+)/$', views.PullFromCMO, name='pullFromCMO'),
    path('assignSiteCommander/', views.assignSiteCommander, name='assignSiteCommander'),
]

urlpatterns = format_suffix_patterns(urlpatterns)