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
        form = LoginForm(request.POST)
        if not form.is_valid():
            raise ValidationError('Invalid data')
        user = authenticate(form.cleaned_data)
        if user:
            print('authentication success')
        else:
            print(f'no such user: {form.cleaned_data}')
            print('will stay in this modal window and popup error message')
        return HttpResponse('login post')
    else:
        return HttpResponse('login get')

def signup(request):
    print(f'signup with method: {request.method}')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            raise ValidationError('Invalid data')
        info = form.cleaned_data
        if info['password'] != info['password_confirmation']:
            raise ValidationError('Passwords do not match')
        else:
            user_info = {k: v for k, v in info.items() if k in ['email', 'password']}
            print('passwords do match')
            user, created = CustomUser.objects.get_or_create(**user_info)
            print(user.__dict__)
            print('created:', created)
        return HttpResponse('signup post')
    else:
        return HttpResponse('signup get')

def logout_view(request):
    return HttpResponse('Logout page')

def enter_view(request):
    template = loader.get_template('registration/enter.html')
    context = dict()
    return HttpResponse(template.render(context, request))
