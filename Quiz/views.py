from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .models import Profile
# Create your views here.


def index(request):
    return HttpResponse('Ritu18')

def UserSignin(request):
    #except invalid passwords
    if request.method == "POST":
        username = request.POST['username']
        password=request.POST['password']
        print(username, password)
        try:
            user=User.objects.get(username=username)
            if user.check_password(password):
                quiz=user.Profile.quiz
                print(quiz)
                url = reverse('test', kwargs={'quiz': quiz})
                print(url)
                return HttpResponseRedirect(url)


            else:
               print('wrong password')
        except User.DoesNotExist:
            print('no  such user ')
    return redirect('/')

def test(request,quiz):
    template = loader.get_template('test.html')
    return HttpResponse(template.render({'quiz':quiz}))