"""Shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views

from my_app.views import index, register, add_to_basket, checkout, buy, lk, view_item, del_all

urlpatterns = [
    url(r'^admin/', admin.site.urls),

# custom urls:
    url(r'^$', index, name='index'),
    url(r'^add_to_basket/(?P<item_id>[0-9]+)/', add_to_basket, name='add_to_basket'),
    url(r'^item/(?P<item_id>[0-9]+)/', view_item, name='view_item'),
    url(r'^del_all/', del_all, name='del_all'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$',auth_views.logout, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^lk/$', lk, name='lk'),

    url(r'^checkout/$', checkout, name='checkout'),
    url(r'^buy/$', buy, name='buy'),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
