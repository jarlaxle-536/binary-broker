from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import *

urlpatterns = [
    path(
        '',
        login_required(AssetListView.as_view()),
        name='asset_list'
    ),
    path(
        'asset/<int:pk>',
        login_required(AssetDetailView.as_view()),
        name='asset_detail'
    ),
    path(
        'asset/update',
        AssetPartialUpdateView.as_view(),
        name='asset_update'
    ),
    path(
        'asset/<int:pk>/get_price_plot/',
        create_price_plot_response,
        name='get_price_plot'
    ),
    path(
        'asset/<int:pk>/create_bet/',
        create_bet,
        name='create_bet'
    )
]
