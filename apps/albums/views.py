from django.core.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_400_BAD_REQUEST, HTTP_200_OK,
                                   HTTP_201_CREATED, HTTP_204_NO_CONTENT)
from rest_framework.views import APIView

from albums.utils import save_photos
from core.decorators import get_user_decorator
from core.utils import extract_exception_text
from users.permissions import IsConfirmed
from albums.models import Photo, Album
from albums.serializers import DynamicPhotoSerializer, PhotoSerializer


class AlbumView(APIView):
    permission_classes = (IsAuthenticated, IsConfirmed)

    def get(self, request, album_id):
        photos = Photo.objects.filter(album=album_id)
        count = photos.count()
        limit = request.GET.get("limit")
        offset = request.GET.get("offset")
        fields = request.GET.get("fields")
        exclude_fields = {"date_created"}
        try:
            if offset:
                photos = photos[int(offset)::]
            if limit:
                limit = int(limit)
                if limit < 50:
                    photos = photos[:limit:]
            else:
                photos = photos[:25:]
            if fields:
                photos = DynamicPhotoSerializer(photos,
                                                many=True,
                                                fields=fields,
                                                exclude_fields=exclude_fields)
            else:
                photos = PhotoSerializer(photos, many=True)
        except (ValueError, OSError, TypeError) as e:
            return Response(str(e), status=HTTP_400_BAD_REQUEST)
        except AssertionError as e:
            if str(e) == "Negative indexing is not supported.":
                return Response({"detail": extract_exception_text(e)},
                                status=HTTP_400_BAD_REQUEST)
        return Response({"photos": photos.data, "count": count},
                        status=HTTP_200_OK)

    @get_user_decorator
    def post(self, request, user, album_id):
        files = request.FILES
        album = get_object_or_404(Album, id=album_id)
        try:
            album.validate_post_request(user=user, files=files)
            photos = save_photos(files=files, user=user, album=album)
            serialized_photos = PhotoSerializer(photos, many=True)
            return Response({"photos": serialized_photos.data},
                            status=HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detail": extract_exception_text(e)},
                            status=HTTP_400_BAD_REQUEST)


class PhotoView(APIView):

    @get_user_decorator
    def delete(self, request, user, album_id, photo_id):
        album = get_object_or_404(Album, id=album_id)
        try:
            album.validate_delete_request(user=user, photo_id=photo_id)
            photo = get_object_or_404(Photo,
                                      user=user,
                                      album=album,
                                      id=photo_id)
            photo.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"detail": extract_exception_text(e)},
                            status=HTTP_400_BAD_REQUEST)
