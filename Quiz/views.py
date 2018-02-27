
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.utils import timezone
from django.utils.datetime_safe import datetime

from .models import Profile, Question, Option, Answers, Quiz, Result


def index(request):
    return HttpResponse('Ritu18')


def UserSignin(request):
    # except related object does no exist user has no profile
    if request.method == "POST":
        try:
            profile = Profile()
            profile.phone = request.POST['phone']
            profile.college = request.POST['college']
            profile.name = request.POST['name']
            profile.quiz = Quiz.objects.get(id=int(request.POST['quiz']))
            profile.save()
            request.session['profile'] = profile.id
        except IntegrityError:
            profile = Profile.objects.get(phone=request.POST['phone'])
            request.session['profile'] = profile.id
            if timezone.now() > profile.started_atempt + profile.quiz.duration:
                return render(request, 'signin.html', {'error': 'Already participated.',
                                                       'quiz_list':Quiz.objects.filter(active=True)})
        return redirect('test', quiz=profile.quiz.id)
    else:
        context = {'quiz_list':Quiz.objects.filter(active=True)}
        return render(request, 'signin.html', context)


def test(request, quiz):
    if 'profile' not in request.session:
        return redirect('UserSignin')
    profile = Profile.objects.get(id=request.session['profile'])
    if timezone.now() > profile.started_atempt + profile.quiz.duration:
        del request.session['profile']
        return HttpResponseForbidden()
    questions = Question.objects.filter(quiz__id=quiz).values('text', 'id')
    quiz_name = Quiz.objects.get(id=quiz).name
    options = []
    for question in questions:
        options += Option.objects.filter(question_id__exact=question['id']).values('value', 'question_id', 'id')
    return render(request, 'test.html', {'quiz': quiz,'quiz_name':quiz_name, 'questions': questions, 'options': options , 'profile' : profile})


def score(request, quiz):
    if 'profile' not in request.session:
        return redirect('UserSignin')
    profile = Profile.objects.get(id=request.session['profile'])
    if profile.quiz_id != int(quiz):
        print(quiz , profile.quiz_id)
        return HttpResponseForbidden()
    if request.method == 'POST':
        template = loader.get_template('end.html')
        try:
            total = 0
            for score_key in filter(lambda key: key.startswith('score'), request.POST.keys()):
                val = int(request.POST[score_key])
                unwanted, question_id = score_key.split('-')
                correct_answer = Option.objects.get(question_id=question_id, is_correct=True)
                answer = Answers(profile=profile, question_id=question_id, option_id=val)
                answer.right = val == correct_answer.id
                answer.save()
                total+= correct_answer.question.score if correct_answer.id == val else 0
                # results = Option.objects.filter(id=val).values('is_correct')
                # for result in results:
                #     result = result['is_correct']
                # Profile_inst = profile
                # new_tuple = Answers(user=Profile_inst, question_id=int(question_id), option_id=val, right=result)
                # if result == True:
                #     points = Question.objects.filter(id=question_id).values('score')
                #     for point in points:
                #         total = total + point['score']
                # Profile_inst = Profile.objects.get(user=user)
                # quiz_inst = Quiz.objects.get(name=quiz)
                # new_result = Result(profile=Profile_inst, quiz=quiz_inst, score=total)
                # new_result.save()
                # new_tuple.save()
            result = Result(quiz_id=quiz, profile=profile,score=total)
            result.save()
        except IntegrityError as e:
            print("inter")
            return HttpResponseForbidden()
        del request.session['profile']
        return redirect('end')
    else:
        return render(request, 'signin.html')


def end(request):
    return render(request,"end.html")