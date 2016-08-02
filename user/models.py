#coding:utf-8
from django.db import models
class Info(models.Model):
    user_name = models.CharField(max_length = 50)
    passWord = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50, null=True)
    #积分
    integral = models.IntegerField(default = 0, null=True)
    #失败次数
    fail_times = models.IntegerField(default = 0, null=True)
    create_time = models.DateTimeField('date published')
    update_time = models.DateTimeField('date published')

# Create your models here.
