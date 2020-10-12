from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import BaseBackend
from social_core.backends.oauth import BaseOAuth2

from .models import CustomUser

class AuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        print('authenticating user with AuthBackend.authenticate')
        if not (email and password): return None
        user = CustomUser.objects.get(email=email)
        if user and user.check_password(password):
            print('AUTHENTIFIED')
            return user
#        print('auth end')
