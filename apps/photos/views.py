from django.core.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_400_BAD_REQUEST, HTTP_200_OK,
                                   HTTP_201_CREATED, HTTP_204_NO_CONTENT)
from rest_framework.views import APIView

from personal_account.custom_permissions import IsConfirmed
from personal_account.models import get_user
from photos.models import Photo, Album
from photos.serializers import DynamicPhotoSerializer, PhotoSerializer


class AlbumView(APIView):
    permission_classes = (IsAuthenticated, IsConfirmed)

    @staticmethod
    def get(request, album_id):
        photos = Photo.objects.filter(album=album_id)
        count = photos.count()
        limit = request.GET.get("limit")
        offset = request.GET.get("offset")
        fields = request.GET.get("fields")
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
                fields = list(fields.split(","))
                fields = list(filter(lambda f: f != "date_added", fields))
                photos = DynamicPhotoSerializer(photos,
                                                many=True,
                                                fields=fields)
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
            photos = []
            for key in tuple(files):
                    Photo.validation(files[key])
                    photo = Photo(user=user, image=files[key], album=album)
                    photos.append(photo)
            Photo.objects.bulk_create(photos)
            photos = PhotoSerializer(photos, many=True)
            return Response({"photos": photos.data}, status=HTTP_201_CREATED)
        except ValidationError:
            return Response(status=HTTP_400_BAD_REQUEST)