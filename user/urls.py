from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'ensureusername/', views.ensureUserName, name='ensureusername'),
    url(r'register/', views.register, name='register'),
    url(r'login/', views.login, name='login'),
    url(r'edit/', views.edit, name='edit'),
    url(r'checkloginstatus/', views.checkLoginStatus, name='checkloginstatus'),
]
