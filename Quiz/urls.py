from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.UserSignin,name='UserSignin'),
    path('test/<quiz>',views.test,name='test'),
    path('score/<quiz>',views.score, name='score'),
    path('end', views.end, name="end")
]