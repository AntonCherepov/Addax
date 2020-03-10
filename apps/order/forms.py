from time import time

from django.forms import CharField, IntegerField, Form

from manuals.models import MasterType, City

now = int(time())


class OrderForm(Form):
    city_id = IntegerField(min_value=1,
                           max_value=City.objects.count())
    request_date_to = IntegerField(min_value=now-10800,
                                   max_value=now+15638400)
    request_date_from = IntegerField(min_value=now-10800,
                                     max_value=now+15638400)
    master_type_id = IntegerField(min_value=1,
                                  max_value=MasterType.objects.count())


class ReplyForm(Form):
    suggested_time_to = IntegerField(min_value=now-10800,
                                     max_value=now+15638400)
    suggested_time_from = IntegerField(min_value=now-10800,
                                       max_value=now+15638400)
    cost = IntegerField(min_value=0, max_value=2147483647)
