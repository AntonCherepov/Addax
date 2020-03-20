from django.core.exceptions import ObjectDoesNotExist, ValidationError

from orders.models import Order


def order_by_id(order_id=None):
    if isinstance(order_id, int):
        try:
            order = Order.objects.get(id=order_id)
            return order
        except ObjectDoesNotExist:
            raise ValidationError(f"No order by {order_id = }")
    else:
        raise ValidationError(f"Invalid order_id")
