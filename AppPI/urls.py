"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib.auth import views
from django.contrib import admin

from PI.views import register, twitter_authenticated, twitter_link, index

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', register, name='register'),
    url(r'^logout/$', views.logout, name='django.contrib.auth.views.logout'),
    url(r'^twitter_link/$', twitter_link, name='twitter_link'),
    url(r'^twitter_authenticated/', twitter_authenticated, name='twitter_authenticated'),
    url(r'^$', index, name='index'),
]
