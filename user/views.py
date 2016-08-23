#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib
import datetime
import json
import redis
import hashlib
import logging
import logging.config
import yaml
import os
from . import forms
from . import models 
# Create your views here.

# init the logger
logger = logging.getLogger('ERMS.user')

#PATH_PYTHON = os.path.dirname(os.path.abspath(__name__))
#PATH_YAML = os.path.join(PATH_PYTHON, 'user/yaml')
#PATH_LOG_CONFIG = os.path.join(PATH_YAML, 'logger.yaml')

#with open(PATH_LOG_CONFIG, 'rt') as f:
#    logging_config = yaml.load(f.read())
#logging.config.dictConfig(logging_config)

#校验用户名是否存在
@csrf_exempt
def EnsureUserName(request):
    retDict = {}
    status = {'code':0,'description':'success'}
    form = forms.UserForm(request.POST)
    if form.is_valid():
        userName = form.cleaned_data['userName']
        users = models.Info.objects.filter(user_name = userName)
        if len(users) > 0:
            status['code'] = '10003'
            status['description'] = '用户名已存在'
    else:
        status['code'] = '10001'
        status['description'] = 'common-fail'
    return HttpResponse(json.dumps(status,ensure_ascii=False))

@csrf_exempt
def Register(request):
    logger.info("request: %s",'testlogging')
    retDict = {}
    status = {'code':0,'description':'success'}
    sid = str()

    form = forms.UserForm(request.POST)
    if form.is_valid():
        userName = form.cleaned_data['userName']
        passWord = form.cleaned_data['passWord']
        user = models.Info(user_name =userName, passWord=passWord)
        now = datetime.datetime.now()
        user.create_time = now
        user.update_time = now
        user.save()
        #保存缓存key:user-sid,value:id
        conn = redis.Redis()
        sid = getSid(user.id, now)  

        conn.set('user-'+sid,user.id)
        print('id=======>>>>>>>',user.id)    
        result = {'userName':userName}
        retDict['result'] = result
    else:
        status['code'] = '10001'
        status['description'] = 'common-fail'

    retDict['status'] = status
    response = HttpResponse(json.dumps(retDict,ensure_ascii=False))
    if sid:
        response.set_cookie('sid',sid)
    return response
@csrf_exempt
def Login(request):
    retDict = {}
    status = {'code':0,'description':'success'}
    conn = redis.Redis()
    sid = str()
    success = True
    fail_ip = str()
    try:
        fail_ip = request.META['HTTP_X_FORWARDED_FOR']
    except KeyError:
        fail_ip = request.META['REMOTE_ADDR']
    if fail_ip is None:
        fail_ip = request.META['REMOTE_ADDR']
    fail_times = conn.get('fail-ip-'+fail_ip)
    total_times = 0
    if fail_times is not None:
        total_times = int(fail_times)
    if total_times > 4:
        status['code'] = '10005'
        status['description'] = '该ip地址禁止登陆,请五分钟后重试！'
        
        retDict['status'] = status
        return HttpResponse(json.dumps(retDict,ensure_ascii=False)) 

    form = forms.UserForm(request.POST)
    if form.is_valid():
        userName = form.cleaned_data['userName']
        passWord = form.cleaned_data['passWord']

        users = models.Info.objects.filter(user_name = userName, passWord = passWord);
        if len(users) > 0:
            user = users[0]
            print(user)
            #取到了保存缓存，没取到记录失败次数，返回错误信息
            #保存缓存key:user-sid,value:id
            now = datetime.datetime.now()
            sid = getSid(user.id, now)

            conn.set('user-'+sid,user.id)
            print(user.id)

            result = {'userName':userName}
            retDict['result'] = result
        else:
            result = {}
            retDict['result'] = result
            status['code'] = '10002'
            status['description'] = '用户名或密码错误!'
            success = False
    else:
        status['code'] = '10001'
        status['description'] = 'common-fail'
        success = False

    if success == 0:
        fail_ip = str()
        try:
            fail_ip = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError:
            fail_ip = request.META['REMOTE_ADDR']
        if fail_ip is None:
            fail_ip = request.META['REMOTE_ADDR']
        conn.incr('fail-ip-'+fail_ip)
        conn.expire('fail-ip-'+fail_ip,60*5)
        

    retDict['status'] = status
    response = HttpResponse(json.dumps(retDict,ensure_ascii=False))
    if sid:
        response.set_cookie('sid',sid)
    return response

@csrf_exempt
def Edit(request):
    retDict = {}
    status = {'code':0,'description':'success'}

    form = forms.UserForm(request.POST)
    if form.is_valid():
        conn = redis.Redis()
        userId = conn.get('user-'+request.COOKIES['sid'])
        user = models.Info.objects.get(id = userId)
        now = datetime.datetime.now()
        user.update_time = now 
        print(user)
        userName = form.cleaned_data['userName']
        passWord = form.cleaned_data['passWord']
        user.user_name = userName
        user.passWord = passWord
        user.save()
    else:
        status['code'] = '10004'
        status['description'] = '数据不合法'
    
    retDict['status'] = status
    return HttpResponse(json.dumps(retDict,ensure_ascii=False))
        
@csrf_exempt
def Index(request):
    return render(request, 'login.html')

def getSid(userId, now):
    src = str(userId) + str(now)
    md5 = hashlib.md5()
    md5.update(src.encode('utf8'))
    sid = md5.hexdigest()
    return sid
