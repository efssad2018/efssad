from django.urls import re_path
from . import views

app_name = "efssad_back"

urlpatterns = [
    #re_path(r'^$/', views.login, name='login'),
    re_path(r'^$', views.login, name='login'),
]