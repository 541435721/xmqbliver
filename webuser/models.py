# coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Webuser(models.Model):
    user = models.OneToOneField(User)  # 用户验证表项
    registerday = models.DateTimeField(auto_now=True, blank=True)  # 注册时间
    identity = models.IntegerField(default=1)  # 用户身份
    online = models.IntegerField(default=False)  # 在线状态
    paid = models.IntegerField(default=False)  # 支付状态
    hospital = models.CharField(max_length=50, null=True, blank=True)# 所在医院

    def __unicode__(self):
        return self.user.username
