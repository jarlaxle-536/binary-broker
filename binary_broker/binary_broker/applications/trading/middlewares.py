from django.conf import settings

def trading_middleware(get_response):
    def core_middleware(request):
        set_commodity_to_trade(request)
        response = get_response(request)
        return response
    return core_middleware

def set_commodity_to_trade(request):
    cmd_key = 'id_of_commodity_to_trade'
    path = request.path
    to_split_by = '/trading/commodity/'
    if path.startswith(to_split_by):
        value = path.split(to_split_by)[-1]
        if value.isdigit():
            request.session[cmd_key] = int(value)
    request.session.setdefault(cmd_key, 1)
