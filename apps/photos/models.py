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


class Workplace(Model):

    photo = ForeignKey(Photo, on_delete=CASCADE)
    master = ForeignKey(MasterAccount, on_delete=CASCADE)


class Gallery(Model):

    photo = ForeignKey(Photo, on_delete=CASCADE)
    master = ForeignKey(MasterAccount, on_delete=CASCADE)
