from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import redirect
from .models import Profile
# Create your views here.


def index(request):
    return HttpResponse('Ritu18')

def UserSignin(request):
    if request.method == "POST":
        username = request.POST['username']
        password=request.POST['password']
        for i in Profile.user:
            print(i)
        #info=Profile.objects.filter(=username).values('user__password','quiz')
        #if info==None:
         #   print('no user ')
        #else:
         #   print(info)


    return redirect('/')