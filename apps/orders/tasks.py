from config.celery import app
from core.smsc_api import SMSC

from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from orders.constants import MASTER_SELECTED, SELECTION_OF_MASTERS
from orders.models import Order, Reply
from users.models import MasterAccount


@app.task(ignore_result=True)
def send_email_order_start(recipient_list: list, message: str,
                           title: str, order_status: str):
    if order_status == MASTER_SELECTED:
        send_mail(title, message, EMAIL_HOST_USER, recipient_list)


@app.task(ignore_result=True)
def send_phone_mail(recipient_number: str, message: str):
    sms = SMSC()
    sms.send_sms('7'+recipient_number, message, sender='sms')


@app.task(ignore_result=True)
def send_new_order_notification(order_id: int) -> None:
    message = 'Доступна новая заявка!'
    title = 'Новая заявка!'
    recipient_list = []

    order = Order.objects.get(id=order_id)
    replies = Reply.objects.filter(order=order)
    replied_masters_raw = replies.values_list('master')
    replied_masters_ids = list(map(lambda v: v[0], replied_masters_raw))
    masters_by_type = MasterAccount.objects.filter(types=order.master_type)
    for master in masters_by_type:
        if master.id not in replied_masters_ids:
            if master.user.email:
                print(master)
                recipient_list.append(master.user.email)
    if recipient_list:
        send_mail(title, message, EMAIL_HOST_USER, recipient_list)


@app.task(ignore_result=True)
def send_new_replies_notification(order_id: int) -> None:
    order = Order.objects.get(id=order_id)
    if order.replies and order.status == SELECTION_OF_MASTERS:
        if order.client.user.email:
            send_mail(
                'Новые отклики!', 'На вашу заявку появились новые отклики!',
                EMAIL_HOST_USER, [order.client.user.email]
            )
