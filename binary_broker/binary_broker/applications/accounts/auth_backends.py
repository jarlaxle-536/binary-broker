from django.contrib.auth.backends import BaseBackend

from .models import CustomUser

class AuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        print('authenticating user with AuthBackend.authenticate')
#        if not (email and password): return None
        user = CustomUser.objects.filter(email=email).first()
        if user and user.check_password(password):
            return user
#        print('auth end')
