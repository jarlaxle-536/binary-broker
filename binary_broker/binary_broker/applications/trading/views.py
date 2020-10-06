from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render

from .models import *

class CommodityListView(ListView):

    template_name = 'commodity/list.html'

    def get_queryset(self):
        return Commodity.objects.all()

class CommodityDetailView(DetailView):
    model = Commodity
    template_name = 'commodity/detail.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context
