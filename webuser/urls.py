# coding:utf-8
# __author__ = 'BianXuesheng'
# __data__ = '2016/07/12_13:48 '

from django.conf.urls import url,include
from django.contrib import admin
from webuser.views import index,register,weblogin,weblogout


urlpatterns = [
    url(r'^$', index),
    url(r'^register/$', register),
    url(r'^login/$', weblogin),
    url(r'^logout/$', weblogout),
]
