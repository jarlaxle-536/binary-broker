from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from bs4 import BeautifulSoup
import json

from .auth_backends import AuthBackend
from .exceptions import *
from .models import *
from .forms import *

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        errors_dict = json.loads(form.errors.as_json())
        user = auth_backend.authenticate(request, **form.cleaned_data)
        if user:
            login(request, user)
        return HttpResponse(json.dumps(errors_dict, ensure_ascii=False))
    else:
        template = loader.get_template('main_page.html')
        return HttpResponse(template.render(dict(), request))

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        errors_dict = json.loads(form.errors.as_json())
        if form.is_valid():
            refined_data = {k: v for k, v in form.cleaned_data.items()
                if k in [k.name for k in CustomUser._meta.fields]}
            user = CustomUser.objects.create_user(**refined_data)
            login(request, user)
        return HttpResponse(json.dumps(errors_dict, ensure_ascii=False))

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    template = loader.get_template('main_page.html')
    return HttpResponse(template.render(dict(), request))

def social_login(request):
    pass

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
