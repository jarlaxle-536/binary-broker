from django.http import HttpResponse
from django.template import loader

from binary_broker.applications.accounts.forms import *

def main(request):
    template = loader.get_template('main_page.html')
    context = dict()
    context['login_form'] = LoginForm()
    context['signup_form'] = SignUpForm()
    return HttpResponse(template.render(context, request))
