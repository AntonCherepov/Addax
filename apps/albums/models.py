from PIL import UnidentifiedImageError, Image
from PIL.Image import DecompressionBombError
from django.core.exceptions import ValidationError
from django.db.models import (Model, DateTimeField, CharField,
                              ForeignKey, ImageField, CASCADE)
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

from config.constants import MAX_ALBUM_COUNTS, ALBUM_TYPE_CHOICES
from users.models import User


class Album(Model):

    user = ForeignKey(User, on_delete=CASCADE)
    type = CharField(max_length=2,
                     choices=ALBUM_TYPE_CHOICES,
                     null=True)

    def validate_count(self, files):
        files_count = len(files)
        if files_count < 1:
            raise ValidationError("No photos in request.")
        photos = Photo.objects.filter(album=self)
        count = photos.count() + files_count
        if count > MAX_ALBUM_COUNTS[self.type]:
            raise ValidationError("Too many photos.")

    def validate_album_exist(self, user):
        if not Album.objects.filter(id=self.id, user=user).exists():
            raise ValidationError("No album with this album_id for current "
                                  "user.")

    def validate_photo_exist(self, user):
        if not Photo.objects.filter(id=self.id, user=user).exists():
            raise ValidationError("No photo with this photo_id for current "
                                  "user.")

    def validate_post_request(self, files, user):
        self.validate_album_exist(user)
        self.validate_count(files)

    def validate_delete_request(self, user):
        self.validate_album_exist(user)
        self.validate_photo_exist(user)


class Photo(Model):

    user = ForeignKey(User, on_delete=CASCADE)
    album = ForeignKey(Album, on_delete=CASCADE, null=True)
    date_created = DateTimeField(auto_now_add=True)
    image = ImageField(upload_to="photo_full")
    image_thumb = ImageSpecField(source='image',
                                 processors=[ResizeToFit(width=600,
                                                         height=600)],
                                 format='JPEG',
                                 options={'quality': 80})

    @staticmethod
    def validate(file):
        try:
            img = Image.open(file)
            if max(img.size) > 5000:
                raise ValidationError("Image is too large")
        except UnidentifiedImageError:
            raise ValidationError("File is not image")
        except DecompressionBombError:
            raise ValidationError("Image size exceeds limit")
