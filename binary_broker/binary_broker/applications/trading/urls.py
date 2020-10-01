from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import *

urlpatterns = [
    path('', login_required(CommodityListView.as_view()), name='commodity_list')
]
