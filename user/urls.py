from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'register/', views.Register, name='register'),
    url(r'login/', views.Login, name='login'),
    url(r'edit/', views.Edit, name='edit'),
    url(r'index/', views.Index, name='index'),
]
