from time import time

from django.forms import CharField, IntegerField, Form

from manuals.models import MasterType, City


class OrderForm(Form):
    city_id = IntegerField(max_value=City.objects.count())
    request_date_to = CharField(max_length=10, min_length=10)
    request_date_from = CharField(max_length=10, min_length=10)
    master_type_code = IntegerField(max_value=MasterType.objects.count())
