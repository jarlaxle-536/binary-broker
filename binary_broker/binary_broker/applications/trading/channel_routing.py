from django.conf.urls import url

from .consumers import *

urlpatterns = [
    url(r"^trading/$", TradingConsumer),
]
