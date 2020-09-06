from distutils.util import strtobool

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Q
from rest_framework.generics import get_object_or_404

from balance.constants import OPERATION_ORDER_COMPLETE
from core.tasks import send_email
from orders.constants import CANCELED_BY_CLIENT, CANCELED_BY_MASTER, SELECTED, \
    MASTER_SELECTED
from orders.models import Order, Reply


def order_by_id(order_id=None):
    if isinstance(order_id, int):
        try:
            order = Order.objects.get(id=order_id)
            return order
        except ObjectDoesNotExist:
            raise ValidationError(f'No order by {order_id = }')
    else:
        raise ValidationError(f'Invalid order_id')


def get_orders_and_master_for_user(request, user, order_exclude_fields):
    exist_master_reply = request.GET.get('exist_master_reply')
    # FixMe
    if user.is_master() and not user.is_client():
        master = user.masteraccount
        order_exclude_fields.add('replies_count')
        master_by_token = request.GET.get('master_by_token')
        if master_by_token is not None:
            master_by_token = strtobool(master_by_token)
        else:
            master_by_token = True
        if master_by_token:
            orders = Order.objects.filter(
                Q(
                    status='sm',
                    master_type__in=master.types.all()
                ) |
                Q(replies__master=master)
            )
        else:
            order_exclude_fields.add('selection_date')
            # Extract orders, where current master reply status
            # isn't "sl" (selected). It is necessary to indicate
            # lost orders.
            exclude_by_replies = Reply.objects.filter(master=master) \
                .filter(status='sl')
            orders = Order.objects.filter(
                master_type__in=master.types.all()) \
                .exclude(replies__in=exclude_by_replies)
        if exist_master_reply is not None:
            if strtobool(exist_master_reply):
                orders = orders.filter(replies__master=master)
            else:
                orders = orders.exclude(replies__master=master)
    elif user.is_client() and not user.is_master():
        master = None
        orders = Order.objects.filter(client=user.clientaccount)
        if exist_master_reply is not None:
            exist_master_reply = not strtobool(exist_master_reply)
            orders = orders.filter(replies__isnull=exist_master_reply)
    else:
        raise ValidationError
    return orders, master


def get_order_by_id_and_master_for_user(request, user,
                                        order_exclude_fields, order_id):
    orders, master = get_orders_and_master_for_user(
        request=request,
        user=user,
        order_exclude_fields=order_exclude_fields
    )
    # FixMe
    # Status 404 isn't correct for all situations
    order = get_object_or_404(orders, id=order_id)
    return order, master


def change_balance_on_complete_order(order, user):
    reply = order.replies.get(master=user.masteraccount)
    difference_value = int(-reply.cost / 10)
    user.balance.change_value(difference_value,
                              OPERATION_ORDER_COMPLETE)


def send_order_status_notification(order):
    title = f'У заявки №{order.id} изменен статус'
    if order.status == CANCELED_BY_CLIENT:
        reply = order.replies.get(status=SELECTED)
        send_email.delay(
            [reply.master.user.email],
            f'Заявка №{order.id} отменена клиентом.',
            title
        )
    elif order.status == CANCELED_BY_MASTER:
        send_email.delay(
            [order.client.user.email],
            f'Заявка  №{order.id} отменена мастером.',
            title
        )
    elif order.status == MASTER_SELECTED:
        reply = order.replies.get(status=SELECTED)
        send_email.delay(
            [reply.master.user.email],
            f'Вас выбрали в заявке №{order.id}.',
            title
        )

