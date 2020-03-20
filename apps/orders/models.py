from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import (Model, CharField, DateTimeField, IntegerField,
                              ForeignKey, CASCADE, SET_NULL, OneToOneField)

from config.constants import ORDER
from manuals.models import City, OrderStatus, ReplyStatus
from users.models import MasterType, ClientAccount, MasterAccount
from albums.models import Album


def order_by_id(order_id=None):
    if isinstance(order_id, int):
        try:
            order = Order.objects.get(id=order_id)
            return order
        except ObjectDoesNotExist:
            raise ValidationError(f"No order by {order_id = }")
    else:
        raise ValidationError(f"Invalid order_id")


class Order(Model):

    master_type = ForeignKey(MasterType, on_delete=SET_NULL, null=True)
    city = ForeignKey(City, on_delete=SET_NULL, null=True)
    status_code = ForeignKey(OrderStatus, on_delete=SET_NULL, null=True)
    date_created = DateTimeField(auto_now_add=True)
    date_modified = DateTimeField(auto_now=True)
    request_date_from = DateTimeField()
    request_date_to = DateTimeField()
    selection_date = DateTimeField(null=True)
    description = CharField(max_length=1000, null=True)
    album = OneToOneField(Album, null=True, on_delete=SET_NULL)
    client = ForeignKey(ClientAccount, on_delete=CASCADE)

    def validate(self):
        if self.request_date_from >= self.request_date_to:
            raise ValidationError("Field \"request_date_from\" can't be more "
                                  "or equal than field \"request_date_to\".")

    def create_album(self):
        a = Album(user=self.client.user, type=ORDER)
        a.save()
        self.album = a


class Reply(Model):

    master = ForeignKey(MasterAccount, on_delete=CASCADE)
    order = ForeignKey(Order, on_delete=CASCADE)
    suggested_time_from = DateTimeField()
    suggested_time_to = DateTimeField()
    cost = IntegerField()
    comment = CharField(max_length=1000, null=True)
    date_created = DateTimeField(auto_now_add=True)
    date_modified = DateTimeField(auto_now=True)
    status = ForeignKey(ReplyStatus, on_delete=SET_NULL, null=True)

    def validate(self):
        if Reply.objects.filter(master=self.master, order=self.order).exists():
            raise ValidationError("Reply already exists.")
        if self.suggested_time_from >= self.suggested_time_to:
            raise ValidationError("Field \"suggested_time_from\" can't be more"
                                  "or equal than field "
                                  "\"suggested_time_from.\"")
