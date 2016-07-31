from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import forms
# Create your views here.
@csrf_exempt
def login(request):
    form = forms.UserForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        return HttpResponse(form.cleaned_data['userName'])

def Index(request):
    return render(request, 'login.html')
