from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import *

urlpatterns = [
    path(
        '',
        login_required(CommodityListView.as_view()),
        name='commodity_list'
    ),
    path(
        'commodity/<int:pk>',
        login_required(CommodityDetailView.as_view()),
        name='commodity_detail'
    ),
    path(
        'commodity/update',
        CommodityPartialUpdateView.as_view(),
        name='commodity_update'
    ),
    path(
        'commodity/<int:pk>/get_price_plot/',
        create_price_plot_response,
        name='get_price_plot'
    ),
]
