from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.template import RequestContext


from .models import Profile,Question,Option



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
                if quiz.active:
                    print(quiz.active)
                    print(quiz)
                    url = reverse('test', kwargs={'quiz': quiz})
                    return HttpResponseRedirect(url)
            else:
               print('wrong password')
        except User.DoesNotExist:
            print('no  such user ')
    return redirect('/')

def test(request,quiz):
    template = loader.get_template('test.html')
    questions=Question.objects.filter(quiz__name=quiz).values('text','id')
    options=[]
    for question in questions:
        options+=Option.objects.filter(question_id__exact=question['id']).values('value','question_id','id')
    return render(request, 'test.html',{'quiz':quiz,'questions':questions,'options':options})
    #return HttpResponse(template.render({'quiz':quiz,'questions':questions,'options':options}))

def score(request):
    if request.method=='POST':
        total= 0
        for score_key in filter(lambda key: key.startswith('score'), request.POST.keys()):
            print(score_key)
            val=int(request.POST[score_key])
            #print(val)
            unwanted, question_id = score_key.split('-')
            #print(question_id)
            results=Option.objects.filter(id=val).values('is_correct')
            for result in results:
                result=result['is_correct']
            if result==True:
                points=Question.objects.filter(id=question_id).values('score')
                for point in points:
                    total=total+point['score']
        print('total:', total)
    return render(request, 'thankyou.html')




