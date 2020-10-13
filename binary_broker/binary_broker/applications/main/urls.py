from django.urls import path

from .views import *

urlpatterns = [
    path('', main, name='main_page'),
    path('set_language/<int:lang_code>', set_language, name='set_language'),
    path('statistics/', statistics, name='statistics'),
    path('ajax/get_time/', get_time, name='get_time'),
]
