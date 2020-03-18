from django.urls import path

from apps.albums.views import AlbumView, PhotoView

urlpatterns = [
    path('<int:album_id>/photos/', AlbumView.as_view()),
    path('<int:album_id>/photos/<int:photo_id>/', PhotoView.as_view()),
]
