from binary_broker.applications.accounts.models import *

def run():
    users = CustomUser.objects.all()
    sep = ' '
    for user in users:
        print('USER:', user)
        for field in user._meta.fields:
            field_name = field.name
            print(sep, field_name, getattr(user, field_name))
