from django.conf import settings

from .models import Commodity

def trading_context_processor(request):
    context = dict()
    context['id_of_commodity_to_trade'] = request.session.get(
        'id_of_commodity_to_trade', 1)
    if request.path.startswith('/trading'):
        context['commodity_list'] = Commodity.objects.all()
    return context
