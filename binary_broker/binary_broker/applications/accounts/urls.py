from django.urls import path, include

from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('', include('social_django.urls', namespace='social')),
    path('set_account_type/', set_account_type, name='set_account_type'),
    path('profile/<int:pk>', user_profile_detail, name='user_profile_detail'),
    path('profile/', user_profile_view, name='user_profile'),
    path('profile/<int:pk>', user_profile_detail, name='user_profile_detail'),
    path('profile/<int:pk>/demo_account', user_profile_demo_account_detail, name='user_profile_demo_account_detail'),
    path('profile/<int:pk>/real_account', user_profile_real_account_detail, name='user_profile_real_account_detail'),
]
