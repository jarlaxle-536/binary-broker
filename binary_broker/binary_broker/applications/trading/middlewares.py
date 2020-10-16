from django.conf import settings

def trading_middleware(get_response):
    def core_middleware(request):
        set_asset_to_trade(request)
        response = get_response(request)
        return response
    return core_middleware

def set_asset_to_trade(request):
    asset_key = 'id_of_asset_to_trade'
    path = request.path
    to_split_by = '/trading/asset/'
    if path.startswith(to_split_by):
        value = path.split(to_split_by)[-1]
        if value.isdigit():
            request.session[asset_key] = int(value)
    request.session.setdefault(asset_key, 1)
