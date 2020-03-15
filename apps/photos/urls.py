from django.urls import path

from apps.photos.views import AlbumView

urlpatterns = [
    path('<int:album_id>/photos/', AlbumView.as_view()),
]
