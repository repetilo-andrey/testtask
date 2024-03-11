from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from coworkers.auth import login_view, logout_view
from coworkers.views import hierarchy, more_coworkers, table_data, table_data_json, coworker_view, coworker_delete_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', hierarchy, name='hierarchy'),
    path('more_coworkers/', more_coworkers, name='more_coworkers'),
    path('table-data/', table_data, name='table_data'),
    path('table_data_json/', table_data_json, name='table_data_json'),

    path('coworkers/', coworker_view, name='coworker_new_view'),
    path('coworkers/<int:coworker_id>/', coworker_view, name='coworker_edit_view'),
    path('coworkers/<int:coworker_id>/delete/', coworker_delete_view, name='coworker_delete_view'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
