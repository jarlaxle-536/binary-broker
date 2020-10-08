from django.apps import apps

def run():
    for model in scrape_models():
        model_intro(model)

def model_intro(model):
    print('*' * 50)
    print(model.__name__.upper())
    print(f'{model._meta.verbose_name} [sng], {model._meta.verbose_name_plural} [plr]')
    print(f'db table name: {model._meta.db_table}')
    related_objects = model._meta.related_objects
    sep = ' ' * 2
    print('Fields:')
    for f in model._meta.fields:
        print(f'{sep}{f.name} [{f.__class__.__name__}]')
    print('Related objects:')
    for ro in related_objects:
        print(f'{sep}{ro.related_model.__name__}.{ro.field.name} [{ro.field.get_internal_type()}]')
    res = [f for f in model._meta.get_fields() if f.is_relation]
    """only 1t1 and fk relations, since direct assignment in m2m is deprecated"""
    rel_fields = [f for f in model._meta.fields]

    for rel_f in rel_fields:
        print('Rel f', rel_f, rel_f.attname)
    get_fields_result = model._meta.get_fields()
    for f in get_fields_result:
        if 'm2m_db_table' in f.__dict__:
            pass

def scrape_models():
    models = list()
    for app in apps.get_app_configs():
        models += app.get_models()
    return models
