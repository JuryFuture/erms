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
import os
from . import forms
from . import models 
# Create your views here.

# init the logger
logger = logging.getLogger('ERMS.user')

#校验用户名是否存在
@csrf_exempt
def ensureUserName(request):
    logger.info('request:%s', request)
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
    retDict['result'] = {}
    return HttpResponse(json.dumps(RetDict,ensure_ascii=False))

@csrf_exempt
def register(request):
    logger.info("request: %s", request)
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
        logger.info('注册用户：%s', user)
        user.save()
        #保存缓存key:user-sid,value:id
        conn = redis.Redis()
        sid = getSid(user.id, now)  

        conn.set('user-'+sid,user.id)
        conn.expire('user-'+sid,60*60*24*7)
        result = {'userName':userName}
        retDict['result'] = result
    else:
        status['code'] = '10001'
        status['description'] = 'common-fail'
        retDict['result'] = {}

    retDict['status'] = status
    response = HttpResponse(json.dumps(retDict,ensure_ascii=False))
    if sid:
        response.set_cookie('sid',sid)
    return response
@csrf_exempt
def login(request):
    logger.info('request：%s', request)
    retDict = {}
    status = {'code':0,'description':'success'}
    result = {}
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
        retDict['result'] = {}
        return HttpResponse(json.dumps(retDict,ensure_ascii=False)) 

    form = forms.UserForm(request.POST)
    if form.is_valid():
        userName = form.cleaned_data['userName']
        passWord = form.cleaned_data['passWord']

        users = models.Info.objects.filter(user_name = userName, passWord = passWord);
        if len(users) > 0:
            user = users[0]
            logger.info('用户：(%s)登陆成功', user)
            #取到了保存缓存，没取到记录失败次数，返回错误信息
            #保存缓存key:user-sid,value:id
            now = datetime.datetime.now()
            sid = getSid(user.id, now)

            conn.set('user-'+sid,user.id)
            conn.expire('user-'+sid,60*60*24*7)

            result = {'userName':userName}
            retDict['result'] = result
        else:
            status['code'] = '10002'
            status['description'] = '用户名或密码错误!'
            success = False
    else:
        status['code'] = '10001'
        status['description'] = 'common-fail'
        success = False

    if success == 0:
        conn.incr('fail-ip-'+fail_ip)
        conn.expire('fail-ip-'+fail_ip,60*5)
        
    retDict['status'] = status
    retDict['result'] = result
    response = HttpResponse(json.dumps(retDict,ensure_ascii=False))
    if sid:
        response.set_cookie('sid',sid)
    return response

@csrf_exempt
def edit(request):
    logger.info('request: %s', request)
    retDict = {}
    status = {'code':0,'description':'success'}
    result = {}

    form = forms.UserForm(request.POST)
    if form.is_valid():
        conn = redis.Redis()
        userId = conn.get('user-'+request.COOKIES['sid'])
        user = models.Info.objects.get(id = userId)
        logger.info('修改前：%s', user)
        now = datetime.datetime.now()
        user.update_time = now
        userName = form.cleaned_data['userName']
        passWord = form.cleaned_data['passWord']
        user.user_name = userName
        user.passWord = passWord
        user.save()
        logger.info('修改后：%s',user)
    else:
        status['code'] = '10004'
        status['description'] = '数据不合法'
    
    retDict['status'] = status
    retDict['result'] = result
    return HttpResponse(json.dumps(retDict,ensure_ascii=False))
        
@csrf_exempt
def checkLoginStatus(request):
    logger.info('request: %s', request)
    retDict = {}
    status = {'code':0,'description':'success'}
    result = {}

    form = forms.LoginCheckForm(request.POST)
    if form.is_valid():
        sid = form.cleaned_data['sid']
        conn = redis.Redis()
        userId = conn.get('user-'+sid)

        if userId == None:
            result['status'] = 0
        else:
            user = models.Info.objects.get(id = userId)
            if user == None:
                status['code'] = 10005
                status['description'] = '用户不存在'
            else:
                result['status'] = 1
    else:
        status['code'] = '10004'
        status['description'] = '数据不合法'
    retDict['status'] = status
    retDict['result'] = result
    return HttpResponse(json.dumps(retDict,ensure_ascii=False))

def getSid(userId, now):
    src = str(userId) + str(now)
    md5 = hashlib.md5()
    md5.update(src.encode('utf8'))
    sid = md5.hexdigest()
    return sid
