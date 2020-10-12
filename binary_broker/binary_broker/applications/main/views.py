from django.shortcuts import redirect
from django.utils import translation
from django.http import HttpResponse
from django.template import loader
from django.conf import settings

from binary_broker.applications.accounts.forms import *
from binary_broker.applications.accounts.models import *

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

def statistics(request):
    template = loader.get_template('statistics.html')
    context = dict()
    users = CustomUser.objects.all()
    users_with_earnings = [(u, sum([
        (lambda s, v: (1 if s else -1) * v)(b.success, b.venture)
        for b in u.profile.bet_set.all() if not b is None])) for u in users]
    users_with_earnings.sort(key=lambda l: l[1], reverse=True)
    context['top_winners'] = users_with_earnings[:10]
    context['top_losers'] = users_with_earnings[-10:]
    return HttpResponse(template.render(context, request))
