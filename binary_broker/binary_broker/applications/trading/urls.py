from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import *

urlpatterns = [
    path('', login_required(CommodityListView.as_view()), name='commodity_list'),
    path('commodity/<int:pk>', login_required(CommodityDetailView.as_view()), name='commodity_detail')
]
