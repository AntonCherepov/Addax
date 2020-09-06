from django.db.models import (Model, ForeignKey, SET_NULL,
                              DateTimeField, CharField, IntegerField, )

from users.models import ClientAccount, MasterAccount


class FeedBack(Model):
    client = ForeignKey(ClientAccount, on_delete=SET_NULL, null=True)
    master = ForeignKey(MasterAccount, on_delete=SET_NULL, null=True)
    date_created = DateTimeField(auto_now_add=True)
    rating = IntegerField(choices=(
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    ))
    nickname = CharField(max_length=50)
    comment = CharField(max_length=2000, null=True)
