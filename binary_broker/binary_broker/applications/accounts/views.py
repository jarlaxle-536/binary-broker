from django.contrib.auth.views import LoginView
from django.http import HttpResponse, JsonResponse
from django.template import loader

from .models import *
from .forms import *

def login_view(request):
    print('trying to login')
    print(f'is ajax: {request.is_ajax()}')
    print(f'method: {request.method}')
    if request.method == 'GET':
        print('and here the modal window comes')
    elif request.method == 'POST':
        print('will parse request to get info')
    return JsonResponse(dict())

def signup_view(request):
    print('trying to signup')
    print(f'is ajax: {request.is_ajax()}')
    return JsonResponse(dict())

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
