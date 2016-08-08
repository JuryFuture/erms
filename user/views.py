#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib
import datetime
import json
import redis
import hashlib
from . import forms
from . import models 
# Create your views here.
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
        src = str(user.id) + str(now)
        md5 = hashlib.md5()
        md5.update(src.encode('utf8'))
        sid = md5.hexdigest()        

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
    sid = str()

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
            conn = redis.Redis()
            now = datetime.datetime.now()
            src = str(user.id) + str(now)
            md5 = hashlib.md5()
            md5.update(src.encode('utf8'))
            sid = md5.hexdigest()

            conn.set('user-'+sid,user.id)
            print(user.id)

            result = {'userName':userName}
            retDict['result'] = result
        else:
            result = {}
            retDict['result'] = result
            status['code'] = '10002'
            status['description'] = '用户不存在!'
    else:
        status['code'] = '10001'
        status['description'] = 'common-fail'

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
