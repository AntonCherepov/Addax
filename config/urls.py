from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

v = "v1/"
urlpatterns = [
    path(v+'admin', admin.site.urls),
    path(v+'users', include('personal_account.urls')),
    path(v+'orders', include('order.urls')),
    path(v+'manuals', include('manuals.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
