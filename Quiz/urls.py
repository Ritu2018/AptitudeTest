from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('UserSignin',views.UserSignin, name='UserSignin'),
    path('test',views.test,name='test')
]