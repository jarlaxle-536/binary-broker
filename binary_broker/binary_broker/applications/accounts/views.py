from django.contrib.auth.views import LoginView
from django.http import HttpResponse

def logout_view(request):
    return HttpResponse('Logout page')

def registration_view(request):
    return HttpResponse('Registration page')
