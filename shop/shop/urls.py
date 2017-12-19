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

from my_app.views import index, register, add_to_basket, checkout, buy, lk, view_item, ajax_add_item, ajax_del_item,  del_all

urlpatterns = [
    url(r'^admin/', admin.site.urls),

# custom urls:
    url(r'^$', index, name='index'),
    url(r'^add_to_basket/(?P<item_id>[0-9]+)/', add_to_basket, name='add_to_basket'),
    url(r'^item/(?P<item_id>[0-9]+)/', view_item, name='view_item'),
    url(r'^ajax_add_item/(?P<item_id>[0-9]+)/', ajax_add_item, name='ajax_add_item'),
    url(r'^ajax_del_item/(?P<item_id>[0-9]+)/', ajax_del_item, name='ajax_del_item'),
    url(r'^del_all/', del_all, name='del_all'),

    url(r'^login/$', auth_views.login, name='login'),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^logout/$',auth_views.logout, name='logout'),
    url(r'^password_reset/$', auth_views.password_reset, {'template_name': 'registration/password_reset_form.html'}, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    url(r'^register/$', register, name='register'),
    url(r'^lk/$', lk, name='lk'),

    url(r'^checkout/$', checkout, name='checkout'),
    url(r'^buy/$', buy, name='buy'),

    url(r'^oauth/', include('social_django.urls', namespace='social'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
