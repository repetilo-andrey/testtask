from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from coworkers.views import main_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
