from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

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
                return render(request, 'test.html',{'quiz':quiz})
            else:
                print('wrong password')
                return redirect('/')
        except User.DoesNotExist:
            print('no  such user ')


def test(request):
    return HttpResponse('yaaay')