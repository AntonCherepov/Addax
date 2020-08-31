from django.utils.datetime_safe import datetime as dt

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import (Model, CharField, DateTimeField, IntegerField,
                              ForeignKey, CASCADE, SET_NULL, OneToOneField)

from config.constants import ORDER
from manuals.models import City
from orders.constants import REPLY_STATUS_CHOICES, ORDER_STATUS_CHOICES
from users.models import MasterType, ClientAccount, MasterAccount
from albums.models import Album


class Order(Model):
    """Order by client."""

    master_type = ForeignKey(MasterType, on_delete=SET_NULL, null=True)
    city = ForeignKey(City, on_delete=SET_NULL, null=True)
    status = CharField(choices=ORDER_STATUS_CHOICES, max_length=2)
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
            raise ValidationError('Field "request_date_from" can\'t be more '
                                  'or equal than field "request_date_to".')

    def create_album(self):
        a = Album(user=self.client.user, type=ORDER)
        a.save()
        self.album = a

    def update_selection_date(self, new_date):
        try:
            new_date = dt.utcfromtimestamp(int(new_date))
            self.selection_date = new_date
        except (ValueError, OSError, OverflowError):
            raise ValidationError('Incorrect value for field "selection_date"')

    def get_reply_by_id(self, reply_id):
        try:
            return self.replies.get(id=reply_id)
        except ObjectDoesNotExist:
            raise ValidationError(f'No reply with {reply_id=} for this order')
        except ValueError:
            raise ValidationError('Incorrect value for field "reply_id"')


class Reply(Model):
    """Reply by master."""

    master = ForeignKey(MasterAccount, on_delete=CASCADE)
    order = ForeignKey(Order, on_delete=CASCADE, related_name='replies')
    suggested_time_from = DateTimeField()
    suggested_time_to = DateTimeField()
    cost = IntegerField()
    comment = CharField(max_length=1000, null=True)
    date_created = DateTimeField(auto_now_add=True)
    date_modified = DateTimeField(auto_now=True)
    status = CharField(choices=REPLY_STATUS_CHOICES, max_length=2)

    def validate(self):
        if Reply.objects.filter(master=self.master, order=self.order).exists():
            raise ValidationError('Reply already exists.')
        if self.suggested_time_from >= self.suggested_time_to:
            raise ValidationError('Field \"suggested_time_from\" can\'t '
                                  'be more or equal than field '
                                  '"suggested_time_from".')
        if self.comment:
            if len(self.comment) > 1000:
                raise ValidationError('Field "comment" is too long.')
