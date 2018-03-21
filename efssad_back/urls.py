from django.urls import path, re_path
from . import views


urlpatterns = [
    path('',views.login, name='login'),
    path('mainmenu/', views.mainmenu, name='mainmenu'),
    path('mcmain/', views.mcmain, name='mcmain'),
    path('scmission/', views.scmission, name='scmission'),
    path('mission/', views.mission, name='mission'),
    path('archive/', views.archive, name='archive'),
    #path('stt/', views.stt, name='stt'),
    re_path(r'^scmission/(?P<missionID>[0-9]+)$', views.scmission, name='scmission'),
    re_path(r'^deployment/(?P<missionID>[0-9]+)$', views.deployment, name='deployment'),
]