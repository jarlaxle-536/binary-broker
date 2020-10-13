from django.conf import settings
from bokeh.resources import CDN
from .views import get_time_dict

def global_settings_processor(request):
    keys = ['LANGUAGES', 'LANGUAGE_CODE']
    settings_dict = {k: getattr(settings, k) for k in keys}
    settings_dict.update(get_time_dict())
    return settings_dict
