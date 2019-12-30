from django.contrib.auth.models import AbstractUser
from django.db.models import (ImageField, CharField, Model,
                              IntegerField, DateTimeField)


class User(AbstractUser):
    """ Модель для пользователей """

    phone_number = CharField('Номер', null=True, max_length=12)
    image = ImageField('Аватарка', upload_to='user_avatars', null=True)

    def get_email(self):
        return self.email

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'


class PhoneCode(Model):
    """ Модель для кода подтверждения пользователя """

    user_id = IntegerField(null=True)
    query_time = DateTimeField(auto_now_add=True)
    code = IntegerField(null=True)
