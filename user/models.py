#coding:utf-8
# Create your models here.
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
    
    def __str__(self):
        return "user_name:"+str(self.user_name)+",passWord:"+str(self.passWord)+",email:"+str(self.email)+",integral:"+str(self.integral)+"fail_times:"+str(self.fail_times)
