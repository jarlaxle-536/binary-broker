from django.urls import path

from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('set_account_type/', set_account_type, name='set_account_type'),
    path('profile/', user_profile_view, name='user_profile')
]
