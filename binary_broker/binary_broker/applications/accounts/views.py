from django.http import HttpResponse

def login_view(request):
    return HttpResponse('Login page')

def logout_view(request):
    return HttpResponse('Logout page')

def registration_view(request):
    return HttpResponse('Registration page')
