from django.views.generic.list import ListView
from django.shortcuts import render

from .models import *

class CommodityListView(ListView):
    template_name = 'commodity/list.html'
    def get_queryset(self):
        return Commodity.objects.all()
