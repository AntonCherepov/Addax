from PIL import UnidentifiedImageError, Image
from PIL.Image import DecompressionBombError
from django.core.exceptions import ValidationError
from django.db.models import (Model, DateTimeField, CharField,
                              ForeignKey, ImageField, CASCADE)
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

from personal_account.models import User


class Album(Model):

    AVATAR = 'AV'
    MASTER_GALLERY = 'MG'
    MASTER_WORKPLACE = 'MW'
    ORDER = 'OR'
    ALBUM_TYPE_CHOICES = [
        (AVATAR, 'Avatar'),
        (MASTER_GALLERY, 'MasterGallery'),
        (MASTER_WORKPLACE, 'MasterWorkPlace'),
        (ORDER, 'Order'),
    ]
    user = ForeignKey(User, on_delete=CASCADE)
    type = CharField(max_length=2,
                     choices=ALBUM_TYPE_CHOICES,
                     null=True)


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
    def validation(file):
        try:
            img = Image.open(file)
            if max(img.size) > 5000:
                raise ValidationError("Image is too large")
        except UnidentifiedImageError:
            raise ValidationError("File is not image")
        except DecompressionBombError:
            raise ValidationError("Image size exceeds limit")
