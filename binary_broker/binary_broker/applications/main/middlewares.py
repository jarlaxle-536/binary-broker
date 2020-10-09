from django.conf import settings

def settings_middleware(get_response):
    def core_middleware(request):
        set_default_language(request)
        response = get_response(request)
        return response
    return core_middleware

def set_default_language(request):
    language_cookie = settings.LANGUAGE_COOKIE_NAME
    print('in set default MW')
    print(f'language cookie: {language_cookie}')
    print(f'settings language code: {settings.LANGUAGE_CODE}')
    if not language_cookie in request.COOKIES:
        request.COOKIES[language_cookie] = settings.LANGUAGE_CODE
    print(f'request cookies: {request.COOKIES}')
