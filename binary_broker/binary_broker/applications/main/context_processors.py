from django.conf import settings

def global_settings_processor(request):
    keys = ['LANGUAGES', 'LANGUAGE_CODE']
    dct = {k: getattr(settings, k) for k in keys}
    print(dct)
    return dct
