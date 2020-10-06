from django.conf import settings

from .models import Commodity

def trading_context_processor(request):
    context = dict()
    if request.path.startswith('/trading'):
        context['commodity_list'] = Commodity.objects.all()
    return context