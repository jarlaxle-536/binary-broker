from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse

from .auth_backends import AuthBackend
from .models import *
from .forms import *

def login_view(request):
    print(f'Login:{request.method}, ajax: {request.is_ajax()}')
    if request.method == 'POST':
        print(request.POST)
        form = LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = auth_backend.authenticate(request, **form.cleaned_data)
            print(user)
            if user:
                login(request, user)
                print(user)
                return redirect(reverse('main_page'))
            else:
                "Make additional error messages [password] pop up"
        else:
            print(form.errors)
            "Return data as JsonResponse"
    template = loader.get_template('main_page.html')
    return HttpResponse(template.render(dict(), request))

def signup_view(request):
    print(f'Signup:{request.method}, ajax: {request.is_ajax()}')
    if request.method == 'POST':
        print(request.POST)
        form = SignUpForm(request.POST)
        if form.is_valid():
            """
                Assuming form detects all signup attempts for existing
                CustomUser with CSRF, so no CustomUser entry in DB for this
                data exists.
            """
            user = CustomUser.objects.create_user(**form.cleaned_data)
            auth_backend.authenticate(request, **form.cleaned_data)
            login(request, user)
            print(user)
            return redirect(reverse('main_page'))
        else:
            print(form.errors)
    template = loader.get_template('main_page.html')
    return HttpResponse(template.render(dict(), request))

def logout_view(request):
    print(f'Logout:{request.method}, ajax: {request.is_ajax()}')
    if request.user.is_authenticated:
        logout(request)
    template = loader.get_template('main_page.html')
    return HttpResponse(template.render(dict(), request))

def enter_view(request):
    template = loader.get_template('registration/enter.html')
    context = dict()
    return HttpResponse(template.render(context, request))

auth_backend = AuthBackend()
