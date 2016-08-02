from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from . import forms
from . import models 
# Create your views here.
@csrf_exempt
def login(request):
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
        
        retDict = {}
        status = {'code':0,'description':'success'}
        
        result = {'userName':userName}
        retDict['status'] = status
        retDict['result'] = result
        return HttpResponse(json.dumps(retDict))

def Index(request):
    return render(request, 'login.html')
