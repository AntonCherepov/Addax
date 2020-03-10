from PIL import UnidentifiedImageError, Image
from PIL.Image import DecompressionBombError
from django.core.exceptions import ValidationError
from django.db.models import (Model, DateTimeField,
                              ForeignKey, ImageField, CASCADE)
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from personal_account.models import User, MasterAccount


class Photo(Model):

    user = ForeignKey(User, on_delete=CASCADE)
    date_created = DateTimeField(auto_now_add=True)
    image = ImageField(upload_to="photo_full")
    image_thumb = ImageSpecField(source='image',
                                 processors=[ResizeToFill(100, 100)],
                                 format='JPEG',
                                 options={'quality': 100})

    @staticmethod
    def validation(file):
        try:
            img = Image.open(file)
            if max(img.size) > 5000:
                raise ValidationError("Image is too large")
        except UnidentifiedImageError:
            raise ValidationError("File is not image")
        except DecompressionBombError:
            raise ValidationError("Image size exceeds limit")


class Workplace(Model):

    photo = ForeignKey(Photo, on_delete=CASCADE)
    master = ForeignKey(MasterAccount, on_delete=CASCADE)


class Gallery(Model):

    photo = ForeignKey(Photo, on_delete=CASCADE)
    master = ForeignKey(MasterAccount, on_delete=CASCADE)
