from django.core.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_400_BAD_REQUEST, HTTP_200_OK,
                                   HTTP_201_CREATED, HTTP_204_NO_CONTENT)
from rest_framework.views import APIView

from albums.utils import create_photos
from users.permissions import IsConfirmed
from users.utils import get_user
from albums.models import Photo, Album
from albums.serializers import DynamicPhotoSerializer, PhotoSerializer


class AlbumView(APIView):
    permission_classes = (IsAuthenticated, IsConfirmed)

    @staticmethod
    def get(request, album_id):
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
                return Response(status=HTTP_400_BAD_REQUEST)
        return Response({"photos": photos.data, "count": count},
                        status=HTTP_200_OK)

    @staticmethod
    def post(request, album_id):
        files = request.FILES
        album = get_object_or_404(Album, id=album_id)
        try:
            user = get_user(request)
            album.validate_post_request(files=files, user=user)
            photos = create_photos(files=files, user=user, album=album)
            serialized_photos = PhotoSerializer(photos, many=True)
            return Response({"photos": serialized_photos.data},
                            status=HTTP_201_CREATED)
        except ValidationError:
            return Response(status=HTTP_400_BAD_REQUEST)


class PhotoView(APIView):

    @staticmethod
    def delete(request, album_id, photo_id):
        user = get_user(request)
        album = get_object_or_404(Album, id=album_id)
        photo = get_object_or_404(Photo,
                                  user=user,
                                  album=album,
                                  id=int(photo_id))
        photo.delete()
        return Response(status=HTTP_204_NO_CONTENT)
