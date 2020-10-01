from django.urls import path

from .views import *

urlpatterns = [
    path('login', login_view, name='login_page'),
    path('logout', logout_view, name='logout_page'),
    path('registration', registration_view, name='registration_page'),
]
