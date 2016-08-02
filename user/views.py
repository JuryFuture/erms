from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from . import forms
from . import models 
# Create your views here.
@csrf_exempt
def login(request):
    form = forms.UserForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        user = models.Info(user_name =form.cleaned_data['userName'],\
            passWord=form.cleaned_data['passWord'])
        now = timezone.now()
        user.create_time = now
        user.update_time = now
        user.save()
        return HttpResponse(form.cleaned_data['userName'])

def Index(request):
    return render(request, 'login.html')
