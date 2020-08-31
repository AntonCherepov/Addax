from config.celery import app
from core.smsc_api import SMSC

from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


@app.task(ignore_result=True)
def send_email(recipient_list: list, message: str, title: str):
    send_mail(title, message, EMAIL_HOST_USER, recipient_list)


@app.task(ignore_result=True)
def send_phone_mail(recipient_number: str, message: str):
    sms = SMSC()
    sms.send_sms('7'+recipient_number, message, sender='sms')
