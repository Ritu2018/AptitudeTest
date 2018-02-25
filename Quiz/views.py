from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate,login

from .models import Profile,Question,Option,Answers,Quiz



def index(request):
    return HttpResponse('Ritu18')

def UserSignin(request):
    #except related object does no exist user has no profile
    if request.method == "POST":
        username = request.POST['username']
        password=request.POST['password']
        try:
            current_user = authenticate(username=username, password=password)
            if current_user is not None:
                if current_user.is_active:
                    login(request,current_user)
                user=request.user
                #print(request.user)
                user_now=User.objects.get(username=user)
                quiz=user_now.Profile.quiz
                if quiz==None:
                    print('no quiz')
                else:
                    #print(quiz)
                    if quiz.active:
                        url = reverse('test', kwargs={'quiz': quiz})
                        return HttpResponseRedirect(url)
                    else:
                        print('no quiz active')
            else:
               print('wrong credentials')
        except User.DoesNotExist:
            print('no  such user ')
    return redirect('/')

def test(request,quiz):
    questions=Question.objects.filter(quiz__name=quiz).values('text','id')
    options=[]
    for question in questions:
        options+=Option.objects.filter(question_id__exact=question['id']).values('value','question_id','id')
    return render(request, 'test.html',{'quiz':quiz,'questions':questions,'options':options})

def score(request):
    if request.method=='POST':
        total= 0
        if request.user.is_authenticated:
            user=request.user
            for score_key in filter(lambda key: key.startswith('score'), request.POST.keys()):
                val=int(request.POST[score_key])
                unwanted, question_id = score_key.split('-')
                results=Option.objects.filter(id=val).values('is_correct')
                for result in results:
                    result=result['is_correct']
                Profile_inst=Profile.objects.filter(user=user).all().first()
                print(Profile_inst, type(Profile_inst))
                new_tuple = Answers(Profile_inst, question_id=int(question_id),option_id= val,right=result)

                new_tuple.save()
                if result==True:
                    points=Question.objects.filter(id=question_id).values('score')
                    for point in points:
                        total=total+point['score']
        print('total:', total)
    return render(request, 'thankyou.html')




