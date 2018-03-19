from django.urls import path, re_path
from . import views


urlpatterns = [
    #re_path(r'^$/', views.login, name='login'),
    #path('', views.login, name='login'),
    path('mainmenu/', views.mainmenu, name='mainmenu'),
    path('mcmain/', views.mcmain, name='mcmain'),
    path('scmission/', views.scmission, name='scmission'),
    path('mission/', views.mission, name='mission'),
    path('archive/', views.archive, name='archive'),
    re_path(r'^deployment/(?P<missionID>[0-9]+)$', views.deployment, name='deployment'),
    # path('deployment/', views.deployment, name='deployment'),
    path('stt/', views.stt, name='stt'),
]