from django.urls import path, re_path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('',views.user, name='user'), #done123
    path('logout/', views.logout, name='logout'),
    path('mainmenu/', views.mainmenu, name='mainmenu'), #done123
    path('mcmain/', views.mcmain, name='mcmain'), #done123
    path('scmission/', views.scmission, name='scmission'), #done123
    # path('mission/', views.mission, name='mission'),
    path('archive/', views.archive, name='archive'),#done123
    path('sendmessage/', views.sendmessage, name='sendmessage'), # done 123
    path('nomissions/', views.nomissions, name='nomissions'),#done123
    path('convertToJSON/', views.convertToJSON, name='convertToJSON'), ##########  NOT DONE Due to JSON ################
    path('searchByMissionID/', views.searchByMissionID, name='searchByMissionID'), #Done222
    #path('stt/', views.stt, name='stt'),
    re_path(r'^scmission/(?P<missionID>-?[0-9]+)$', views.scmissionID, name='scmissionID'), #done222
    re_path(r'^deployment/(?P<missionID>[0-9]+)$', views.deployment, name='deployment'), #done222
    re_path(r'^archiveDetail/(?P<missionID>[0-9]+)$', views.archiveDetail, name='archiveDetail'), #done222
    re_path(r'^missionDetail/(?P<missionID>[0-9]+)$', views.missionDetail, name='missionDetail'), #done2222
    re_path(r'^updateStatus/(?P<missionID>[0-9]+)/(?P<status>\w+)$', views.updateStatus, name='updateStatus'), # 2222
    re_path(r'^missions/$', views.MissionList.as_view()),##########  NOT DONE Due to API ################
    re_path(r'^missions/(?P<pk>[0-9]+)/$', views.MissionDetail.as_view()),##########  NOT DONE Due to API ################
    re_path(r'^messagelogs/$', views.MessageLogList.as_view()),##########  NOT DONE Due to API ################
    re_path(r'^messagelogs/(?P<pk>[0-9]+)/$', views.MessageLogDetail.as_view()),##########  NOT DONE Due to API ################
    re_path(r'^plans/$', views.PlanList.as_view()),##########  NOT DONE Due to PLAN ################
    re_path(r'^plans/(?P<pk>[0-9]+)/$', views.PlanDetail.as_view()), ##########  NOT DONE Due to PLAN ################
    re_path(r'^updates/$', views.UpdateList.as_view()),##########  NOT DONE Due to PLAN ################
    re_path(r'^updates/new/$', views.UpdateNew.as_view()),##########  NOT DONE Due to PLAN ################
    # re_path(r'^updates/new/(?P<pk>[0-9]+)/$', views.UpdatePull),
    re_path(r'^test/new/(?P<pk>[0-9]+)/$', views.PullFromCMO, name='pullFromCMO'),
    path('assignSiteCommander/', views.assignSiteCommander, name='assignSiteCommander'),#done 222
    path('updateMsgLog/', views.updateMsgLog, name='updateMsgLog'),
    path('ajax/', views.testAjax, name='testAjax'), #done123
    path('saveplan/', views.saveplan, name='saveplan'),
    path('savenewmission/', views.savenewmission, name='savenewmission'),
]

urlpatterns = format_suffix_patterns(urlpatterns)