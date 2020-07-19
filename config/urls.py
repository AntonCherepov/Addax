from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

v = "v1/"
urlpatterns = [
    path(v+'admin/', admin.site.urls),
    path(v+'users/', include('users.urls')),
    path(v+'orders/', include('orders.urls')),
    path(v+'manuals/', include('manuals.urls')),
    path(v+'albums/', include('albums.urls')),
    path('v2/', include('feedbacks.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
