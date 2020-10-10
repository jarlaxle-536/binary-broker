from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from bs4 import BeautifulSoup
import json

from .auth_backends import AuthBackend
from .models import *
from .forms import *

def login_view(request):
    print(f'Login:{request.method}, ajax: {request.is_ajax()}')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        errors_dict = json.loads(form.errors.as_json())
        print(form)
        user = auth_backend.authenticate(request, **form.cleaned_data)
        print(errors_dict)
        if user:
            login(request, user)
        elif not 'no_such_user' in [e['code']
            for e in errors_dict.get('email', list())]:
            errors_dict['password'] = [{
                "message": "PasswordIsIncorrect",
                "code": "incorrect_password"
            }]
        return HttpResponse(json.dumps(errors_dict, ensure_ascii=False))

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
            raise Exception('Form invalid')
            "Return data as JsonResponse"
    template = loader.get_template('main_page.html')
    return HttpResponse(template.render(dict(), request))

def logout_view(request):
    print(f'Logout:{request.method}, ajax: {request.is_ajax()}')
    if request.user.is_authenticated:
        logout(request)
    template = loader.get_template('main_page.html')
    return HttpResponse(template.render(dict(), request))

@login_required
def set_account_type(request):
    new_account_type = Profile.get_account_choice(request.POST['account_type'])
    user_profile = request.user.profile
    user_profile.chosen_account = new_account_type
    user_profile.save()
    print(user_profile.chosen_account)
    return HttpResponse('lorem ipsum')

def user_info_detail(request, **kwargs):
    spec = kwargs['spec']
    template_name = f'user_profile_{spec}_detail.html'.replace('__', '_')
    template = loader.get_template(template_name)
    context = dict()
    return HttpResponse(template.render(context, request))

def user_profile_detail(request, **kwargs):
    template = loader.get_template('user_profile_detail.html')
    context = dict()
    return HttpResponse(template.render(context, request))

def user_profile_demo_account_detail(request, **kwargs):
    template = loader.get_template('user_profile_demo_account_detail.html')
    context = dict()
    return HttpResponse(template.render(context, request))

def user_profile_real_account_detail(request, **kwargs):
    template = loader.get_template('user_profile_real_account_detail.html')
    context = dict()
    return HttpResponse(template.render(context, request))

@login_required
def user_profile_view(request):
    template = loader.get_template('user_profile_detail.html')
    context = dict()
    return HttpResponse(template.render(context, request))

auth_backend = AuthBackend()
