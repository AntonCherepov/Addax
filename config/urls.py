from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

v = "v1/"
urlpatterns = [
    # path(''),
    path('admin/', admin.site.urls),
    path('users/', include('personal_account.urls')),
    path('orders/', include('order.urls')),
    path('manuals/', include('manuals.urls')),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
