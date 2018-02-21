from django.http.response import HttpResponse
from django.shortcuts import render

def index(request):
    #ritu poster
    return render(request, 'index.html')

def signin(request):
    return render(request, 'signin.html')