from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout
from django.shortcuts import render
from django.template import loader

from .auth_backends import AuthBackend
from .models import *
from .forms import *

def login_view(request):
    print(f'Login:{request.method}, ajax: {request.is_ajax()}')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth_backend.authenticate(request, **form.cleaned_data)
            if user:
                login(request, user)
            else:
                "Make additional error messages [password] pop up"
            "Return data as JsonResponse"
    template = loader.get_template('main_page.html')
    return HttpResponse(template.render(dict(), request))

def signup_view(request):
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

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    template = loader.get_template(request.GET['HTTP_REFERER'])
    return HttpResponse(template.render(dict(),))

def enter_view(request):
    template = loader.get_template('registration/enter.html')
    context = dict()
    return HttpResponse(template.render(context, request))

auth_backend = AuthBackend()
