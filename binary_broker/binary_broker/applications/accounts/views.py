from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.template import loader

from .models import *
from .forms import *

def registration_view(request):
    template = loader.get_template('registration/login.html')
    context = {'form': RegisterForm()}
    return HttpResponse(template.render(context, request))

def logout_view(request):
    return HttpResponse('Logout page')

def enter_view(request):
    template = loader.get_template('registration/enter.html')
    context = dict()
    return HttpResponse(template.render(context, request))

def get_login_form(request):
    print('getting login form')
    context = {'form': LoginForm()}
    print(context)

def get_signup_form(request):
    print('getting signup form')
    context = {'form': SignUpForm()}
    print(context)
