from django.conf import settings

from .auxiliary import *

def global_settings_processor(request):
    keys = ['LANGUAGES', 'LANGUAGE_CODE']
    settings_dict = {k: getattr(settings, k) for k in keys}
    settings_dict['language_names'] = dict(settings_dict['LANGUAGES'])
    settings_dict.update(get_time_dict())
    return settings_dict
