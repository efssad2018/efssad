from django.urls import path, re_path
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
    #path('stt/', views.stt, name='stt'),
    re_path(r'^scmission/(?P<missionID>-?[0-9]+)$', views.scmissionID, name='scmissionID'),
    re_path(r'^deployment/(?P<missionID>[0-9]+)$', views.deployment, name='deployment'),
    re_path(r'^archiveDetail/(?P<missionID>[0-9]+)$', views.archiveDetail, name='archiveDetail'),
    re_path(r'^missionDetail/(?P<missionID>[0-9]+)$', views.missionDetail, name='missionDetail'),
    re_path(r'^updateStatus/(?P<missionID>[0-9]+)/(?P<status>\w+)$', views.updateStatus, name='updateStatus'),
]