from django.conf import settings

def global_settings_processor(request):
    keys = ['LANGUAGES', 'LANGUAGE_CODE']
    global_settings_dict = {k: getattr(settings, k) for k in keys}
    return global_settings_dict
