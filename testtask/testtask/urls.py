from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from coworkers.views import main_page, more_coworkers


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page),
    path('more_coworkers/', more_coworkers, name='more_coworkers'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
