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
    print(request.session.get(cmd_key, None))
    if path.startswith(to_split_by):
        commodity_id = int(path.split(to_split_by)[-1])
        request.session[cmd_key] = commodity_id
    request.session.setdefault(cmd_key, 1)
    print('cmd to trade:', request.session[cmd_key])
