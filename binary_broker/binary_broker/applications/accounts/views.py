from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.template import loader

from .models import *
from .forms import *

def login(request):
    print(f'login with method: {request.method}')
    if request.method == 'POST':
        if not request.is_ajax():
            return JsonResponse(request.POST)
        user_info = LoginForm(request.POST).clean()
        user = authenticate(**user_info)
        if user:
            print('authentication success')
        else:
            print(f'no such user: {info}')
            print('will stay in this modal window and popup error message')
        return HttpResponse(request)
    else:
        return HttpResponse('login get')

def login(request):
    print('will initiate ajax request to some handler')
    template = loader.get_template('main_page.html')
    return HttpResponse(template.render(dict(), request))

def signup(request):
    print(f'signup with method: {request.method}')
    if request.method == 'POST':
        print(request.POST)
#        if not request.is_ajax():
#            return JsonResponse(request.POST)
        form = SignUpForm(request.POST)
        if form.is_valid():
            user_info = {k: v for k, v in form.cleaned_data.items()
                if k in ['email', 'password']}
            user, created = CustomUser.objects.get_or_create(**user_info)
            print(user.__dict__)
            print('created:', created)
            return HttpResponse('signup post')
        else:
            return HttpResponse(request)
    else:
        return HttpResponse('signup get')

def logout_view(request):
    return HttpResponse('Logout page')

def enter_view(request):
    template = loader.get_template('registration/enter.html')
    context = dict()
    return HttpResponse(template.render(context, request))
