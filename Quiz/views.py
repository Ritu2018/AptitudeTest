from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
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
                user_now=User.objects.get(username=user) #type User
                template = loader.get_template('quiz_list.html')
                quiz_list=user_now.Profile.quiz.values()
                if len(quiz_list)==0:
                    print('no quiz')
                else:
                    quiz_context=[]
                    for quiz in quiz_list:
                        print('quiz:',quiz)
                        if quiz['active']:
                            quiz_context.append(quiz['name'])
                            print(quiz['name'])
                        #else:
                         #   print('no quiz active')
                      #url = reverse('test', kwargs={'quiz': quiz})

                    return HttpResponse(template.render({'quiz_list':quiz_context}))

            else:
               print('wrong credentials')
        except User.DoesNotExist:
            print('no  such user ')
    else:
        return render(request,'signin.html')

def test(request,quiz):
    questions=Question.objects.filter(quiz__name=quiz).values('text','id')
    options=[]
    for question in questions:
        options+=Option.objects.filter(question_id__exact=question['id']).values('value','question_id','id')
    return render(request, 'test.html',{'quiz':quiz,'questions':questions,'options':options})

def score(request):
    if request.method=='POST':
        try:
            total= 0
            if request.user.is_authenticated:
                user=request.user
                for score_key in filter(lambda key: key.startswith('score'), request.POST.keys()):
                    val=int(request.POST[score_key])
                    unwanted, question_id = score_key.split('-')
                    results=Option.objects.filter(id=val).values('is_correct')
                    for result in results:
                        result=result['is_correct']
                    Profile_inst=Profile.objects.get(user=user)
                    print(Profile_inst, type(Profile_inst))
                    new_tuple = Answers(user=Profile_inst, question_id=int(question_id),option_id= val,right=result)
                    print(new_tuple)
                    new_tuple.save()
                    if result==True:
                        points=Question.objects.filter(id=question_id).values('score')
                        for point in points:
                            total=total+point['score']
                Profile_inst = Profile.objects.get(user=user)
                Profile_inst.total_score = total
                Profile_inst.save()
            print('total:', total)

        except IntegrityError as e:
            print('already submitted')
        logout(request)
    return render(request, 'thankyou.html')


def quiz_list(request):
    pass

