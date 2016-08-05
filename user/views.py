#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
import redis
import hashlib
from . import forms
from . import models 
# Create your views here.
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
        status['code'] = '0001'
        status['description'] = 'common-fail'

    retDict['status'] = status
    response = HttpResponse(json.dumps(retDict))
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

        user = models.Info.objects.filter(userName = userName, passWord = passWord);
        #取到了保存缓存，没取到记录失败次数，返回错误信息
        #保存缓存key:user-sid,value:id
        conn = redis.Redis()
        src = str(user.id) + str(now)
        md5 = hashlib.md5()
        md5.update(src.encode('utf8'))
        sid = md5.hexdigest()

        conn.set('user-'+sid,user.id)
        print(user.id)

        result = {'userName':userName}
        retDict['result'] = result
    else:
        status['code'] = '0001'
        status['description'] = 'common-fail'

    retDict['status'] = status
    response = HttpResponse(json.dumps(retDict))
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
        userId = conn.get('user-'+reqest.session.session_key)
        user = models.Info.objects.get(id = userId)
        now = datetime.datetime.now()
        user.update_time = now 
    else:
        pass
    
    retDict['status'] = status
    return HttpResponse(json.dumps(retDict))
        
@csrf_exempt
def Index(request):
    return render(request, 'login.html')
