from time import time

from django.forms import CharField, IntegerField, Form

from manuals.models import MasterType, City


class OrderForm(Form):
    city_id = IntegerField(max_value=City.objects.count())
    request_date_to = CharField(max_length=10, min_length=10)
    request_date_from = CharField(max_length=10, min_length=10)
    master_type_id = IntegerField(max_value=MasterType.objects.count())


class ReplyForm(Form):
    suggested_time_from = CharField(max_length=10, min_length=10)
    suggested_time_to = CharField(max_length=10, min_length=10)
    cost = IntegerField(min_value=0, max_value=2147483647)
