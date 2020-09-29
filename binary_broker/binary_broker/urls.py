from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('binary_broker.applications.main.urls')),
    path('trading/', include('binary_broker.applications.trading.urls'))
]
