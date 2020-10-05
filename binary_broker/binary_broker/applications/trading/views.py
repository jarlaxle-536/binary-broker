from django.views.generic.list import ListView
from django.shortcuts import render

from .models import *

class CommodityListView(ListView):

    template_name = 'commodity/list.html'

    def get_queryset(self):
        return Commodity.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context
