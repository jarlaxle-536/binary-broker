from django.urls import path

from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_page'),
    path('logout/', logout_view, name='logout_page'),
    path('registration/', registration_view, name='registration_page'),
    path('enter/', enter_view, name='enter_page')
]
