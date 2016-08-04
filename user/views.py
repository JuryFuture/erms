#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from . import forms
from . import models 
# Create your views here.
@csrf_exempt
def Register(request):
    retDict = {}
    status = {'code':0,'description':'success'}

    form = forms.UserForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        userName = form.cleaned_data['userName']
        passWord = passWord=form.cleaned_data['passWord']
        user = models.Info(user_name =userName, passWord=passWord)
        now = timezone.now()
        user.create_time = now
        user.update_time = now
        user.save()
        #保存缓存key:user-sid,value:id
        print('id=======>>>>>>>',user.id)    
        result = {'userName':userName}
        retDict['result'] = result

    retDict['status'] = status
    return HttpResponse(json.dumps(retDict))
@csrf_exempt
def Login(request):
    retDict = {}
    status = {'code':0,'description':'success'}

    form = forms.UserForm(request.POST)
    if form.is_valid():
        userName = form.cleaned_data['userName']
        passWord = passWord=form.cleaned_data['passWord']

        user = models.info.objects.filter(userName = userName, passWord = passWord);
        print(user)

        result = {'userName':userName}
        retDict['result'] = result

    retDict['status'] = status
    return HttpResponse(json.dumps(retDict))

@csrf_exempt
def Edit(request):
    retDict = {}
    status = {'code':0,'description':'success'}
    retDict['status'] = status
    return HttpResponse(json.dumps(retDict))
        
@csrf_exempt
def Index(request):
    return render(request, 'login.html')
