from django.conf import settings

from .forms import *
from .models import Profile

def auth_context_processor(request):
    keys = [
        'API_SECRETS',
    ]
    context = {k: getattr(settings, k) for k in keys}
    context['oauth_providers'] = list(context['API_SECRETS'])
    context['oauth_backends'] = {
        'google': 'google-oauth2',
        'facebook': 'facebook',
        'github': 'github',
    }
    context['oauth_logo_paths'] = {p: f'images/{p}_logo.png'
        for p in context['oauth_providers']}
    context['login_form'] = LoginForm()
    context['signup_form'] = SignUpForm()
    context['account_type_form'] = ProfileAccountTypeForm()
    if 'profile' in request.path:
        profile_id = (lambda s: int(s) if s else request.user.profile.id)(
            request.path.split('profile/')[1].split('/')[0])
        context['profile'] = Profile.objects.filter(id=profile_id).first()
    return context
