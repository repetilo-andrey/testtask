from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from coworkers.views import main_page, more_coworkers, table_data, table_data_json


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page),
    path('more_coworkers/', more_coworkers, name='more_coworkers'),
    path('table-data/', table_data, name='table_data'),
    path('table_data_json/', table_data_json, name='table_data_json'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
