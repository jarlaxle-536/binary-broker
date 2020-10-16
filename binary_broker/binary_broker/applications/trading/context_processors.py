from django.conf import settings

from .models import *

def trading_context_processor(request):
    context = dict()
    context['id_of_asset_to_trade'] = request.session.get(
        'id_of_asset_to_trade', 1)
    if request.path.startswith('/trading'):
        context['asset_list'] = Asset.objects.all()
    return context
