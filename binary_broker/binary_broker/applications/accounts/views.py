from django.contrib.auth import decorators, authenticate, logout
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.template import loader

from .models import *
from .forms import *

def login(request):
    if request.method == 'GET':
        template = loader.get_template('main_page.html')
        return HttpResponse(template.render(dict(), request))
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        print('form valid:', form.is_valid())
        is_form_valid = form.is_valid()
        if is_form_valid:
            user_info = form.cleaned_data
            user = authenticate(request, **user_info)
            if user:
                login(request, user)
                print('authentication success')
            else:
                print(f'no such user: {user_info}')
                print('will stay in this modal window and user not found message')
        else:
            print(form.cleaned_data)
        template = loader.get_template('main_page.html')
        return HttpResponse(template.render(dict(), request))

def signup(request):
    if request.method == 'POST':
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

#@decorators.login_required
def logout(request):
    print('Calling logout')
    print('User authenticated:', request.user.is_authenticated)
    if request.user.is_authenticated:
        print('LOGGING USER OUT')
        logout(request)
    template = loader.get_template('main_page.html')
    return HttpResponse(template.render(dict(),))

def enter_view(request):
    template = loader.get_template('registration/enter.html')
    context = dict()
    return HttpResponse(template.render(context, request))
