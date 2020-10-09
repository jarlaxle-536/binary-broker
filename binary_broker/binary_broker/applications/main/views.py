from django.shortcuts import redirect
from django.utils import translation
from django.http import HttpResponse
from django.template import loader
from django.conf import settings

from binary_broker.applications.accounts.forms import *

def main(request):
    template = loader.get_template('main_page.html')
    context = dict()
    context['login_form'] = LoginForm()
    context['signup_form'] = SignUpForm()
    return HttpResponse(template.render(context, request))

def set_language(request, lang_code):
    print(f'set language with {lang_code}')
    language = settings.LANGUAGES[lang_code][0]
    print(f'languages: {settings.LANGUAGES}')
    print(f'new language: {language}')
    translation.activate(language)
    response = redirect(request.META['HTTP_REFERER'])
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response
