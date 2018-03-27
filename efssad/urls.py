"""efssad URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
# from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from efssad_back import views

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('efssad_back.urls')),
    # re_path(r'^', include(router.urls)),
    # re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # re_path(r'^missions/', views.MissionList.as_view()),
    # re_path(r'^missions/(?P<pk>[0-9]+)/', views.MissionDetail.as_view()),
    # re_path(r'^messagelogs/', views.MessageLogList.as_view()),
    # re_path(r'^plans/', views.PlanList.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
