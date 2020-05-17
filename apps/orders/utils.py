from distutils.util import strtobool

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Q

from orders.models import Order, Reply


def order_by_id(order_id=None):
    if isinstance(order_id, int):
        try:
            order = Order.objects.get(id=order_id)
            return order
        except ObjectDoesNotExist:
            raise ValidationError(f"No order by {order_id = }")
    else:
        raise ValidationError(f"Invalid order_id")


def get_orders_and_master_for_user(request, user, order_exclude_fields):
    # FixMe
    if user.is_master() and not user.is_client():
        master = user.masteraccount
        order_exclude_fields.add("replies_count")
        master_by_token = request.GET.get("master_by_token")
        if master_by_token is not None:
            master_by_token = strtobool(master_by_token)
        else:
            master_by_token = True
        if master_by_token:
            orders = Order.objects.filter(
                Q(
                    status="sm",
                    master_type__in=master.types.all()
                ) |
                Q(replies__master=master)
            )
        else:
            order_exclude_fields.add("selection_date")
            # Extract orders, where current master reply status
            # isn't "sl" (selected). It is necessary to indicate
            # lost orders.
            exclude_by_replies = Reply.objects.filter(master=master) \
                .filter(status="sl")
            orders = Order.objects.filter(
                master_type__in=master.types.all()) \
                .exclude(replies__in=exclude_by_replies)
    elif user.is_client() and not user.is_master():
        master = None
        orders = Order.objects.filter(client=user.clientaccount)
    else:
        raise ValidationError
    return orders, master
