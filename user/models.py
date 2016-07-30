from django.db import models
class Info(models.Model):
    user_name = models.CharField(max_length = 20)
    passWord = models.CharField(max_length = 20)
    email = models.CharField(max_length = 40)
    create_time = models.DateTimeField('date published')
    update_time = models.DateTimeField('date published')
    integral = models.IntegerField(default = 0)
# Create your models here.
