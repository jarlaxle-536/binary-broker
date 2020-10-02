from django.conf import settings

from .forms import *

def auth_context_processor(request):
    keys = [
        'API_SECRETS',
    ]
    context = {k: getattr(settings, k) for k in keys}
    context['oauth_providers'] = list(context['API_SECRETS'])
    context['oauth_logo_paths'] = {p: f'images/{p}_logo.png'
        for p in context['oauth_providers']}
    context['login_form'] = LoginForm()
    context['signup_form'] = SignUpForm()
    return context
