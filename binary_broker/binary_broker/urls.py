from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),

    path('accounts/', include('binary_broker.applications.accounts.urls')),
    path('trading/', include('binary_broker.applications.trading.urls')),
    path('', include('binary_broker.applications.main.urls')),
]
