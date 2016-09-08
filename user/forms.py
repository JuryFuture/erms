from django import forms

class UserForm(forms.Form):
    userName = forms.CharField(max_length=100)
    passWord = forms.CharField(max_length=100)

class LoginCheckForm(forms.Form):
    sid = forms.CharField(max_length=100)
