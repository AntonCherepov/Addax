from time import time

from django.forms import CharField, IntegerField, Form


class OrderForm(Form):
    description = CharField(max_length=1000)
    city = IntegerField()
    request_date_to = IntegerField(min_value=int(time()),
                                   max_value=99999999999)
    request_date_from = IntegerField(min_value=int(time()),
                                     max_value=99999999999)
    master_type = IntegerField()
