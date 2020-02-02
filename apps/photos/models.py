from django.db.models import (Model, IntegerField, DateTimeField,
                              ForeignKey, ImageField, CASCADE)

from personal_account.models import User, MasterAccount


class Photo(Model):

    user = ForeignKey(User, on_delete=CASCADE)
    date_created = DateTimeField(auto_now_add=True)
    image = ImageField(upload_to="photo_full")
    image_thumb = ImageField(upload_to="photo_thumb")


class Workplace(Model):

    photo = ForeignKey(Photo, on_delete=CASCADE)
    master = ForeignKey(MasterAccount, on_delete=CASCADE)


class Gallery(Model):

    photo = ForeignKey(Photo, on_delete=CASCADE)
    master = ForeignKey(MasterAccount, on_delete=CASCADE)
