from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import (CharField, Model, CASCADE,
                              IntegerField, DateTimeField, ForeignKey,
                              OneToOneField, ManyToManyField,)

from config.constants import AVATAR, MASTER_WORKPLACE, MASTER_GALLERY
from core.utils import get_possible_choice_values
from users.constants import (USER_TYPE_CHOICES, USER_STATUS_CHOICES,
                             USER_REGISTERED, USER_BANNED,
                             USER_CONFIRMED, MASTER_STATUS_CHOICES,
                             MASTER_UNVERIFIED)
from manuals.models import MasterType


class User(AbstractUser):
    """ Модель для пользователей """

    phone_number = CharField('Номер', null=True, max_length=10, unique=True)
    type_code = CharField(choices=USER_TYPE_CHOICES, max_length=2)
    status = CharField(choices=USER_STATUS_CHOICES, max_length=2)
    date_modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number

    def is_banned(self):
        banned_status = USER_BANNED
        return True if self.status == banned_status else False

    def is_confirmed(self):
        confirmed_status = USER_CONFIRMED
        return True if self.status == confirmed_status else False

    def is_master(self):
        return hasattr(self, "masteraccount")

    def is_client(self):
        return hasattr(self, "clientaccount")

    def validate_phone(self):
        try:
            int(str(self.phone_number))
        except ValueError:
            raise ValidationError('phone_number is not a number')
        if str(self.phone_number)[0] != "9":
            raise ValidationError('Incorrect phone_number')
        try:
            if user := User.objects.get(phone_number=self.phone_number):
                if not user.is_banned():
                    raise ValidationError('User with this phone_number '
                                          'already exists')
                raise ValidationError('User is banned')
        except ObjectDoesNotExist:
            pass

    def validate_type_code(self):
        if self.type_code not in get_possible_choice_values(USER_TYPE_CHOICES):
            raise ValidationError('Incorrect type_code')

    def validate_confirmation_request(self):
        users = User.objects.filter(phone_number=self.phone_number)
        if users.count() > 1:
            raise ValidationError('Too many users')
        elif not users.exists():
            raise ValidationError('User with this phone_number does not '
                                  'exists')
        elif self.status != USER_REGISTERED:
            raise ValidationError("User does not need confirmation")

    def validate_registration_request(self):
        self.validate_phone()
        self.validate_type_code()

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'


class PhoneCode(Model):
    """ Модель для кода подтверждения пользователя """

    user = ForeignKey(User, on_delete=CASCADE)
    query_time = DateTimeField(auto_now_add=True)
    code = IntegerField(null=True)

    def __str__(self):
        return self.code

    def validate(self):
        confirm_codes = PhoneCode.objects.filter(user=self.user)
        if confirm_codes.exists():
            confirm_code = confirm_codes.order_by("-id")[:1:][0]
            time_difference = timezone.now() - confirm_code.query_time
            if self.code != confirm_code.code:
                raise ValidationError('Incorrect code')
            elif time_difference.seconds > 305:
                raise ValidationError('Code is too old')
            else:
                return confirm_codes[0]
        else:
            raise ValidationError('No confirm codes for user')


class MasterAccount(Model):

    user = OneToOneField(User, on_delete=CASCADE)
    types = ManyToManyField(MasterType)
    about_myself = CharField(null=True, max_length=10000)
    status = CharField(choices=MASTER_STATUS_CHOICES, max_length=2)
    name = CharField(max_length=100)
    address = CharField(max_length=250)

    def create_account(self):
        from albums.models import Album
        from balance.models import Balance

        if ClientAccount.objects.filter(user=self.user).exists():
            return False
        elif not MasterAccount.objects.filter(user=self.user).exists():
            p = MasterAccount(user=self.user, status=MASTER_UNVERIFIED)
            Album.objects.bulk_create(
                [
                    Album(user=self.user, type=AVATAR),
                    Album(user=self.user, type=MASTER_WORKPLACE),
                    Album(user=self.user, type=MASTER_GALLERY),
                ]
            )
            Balance.objects.create(user=self.user, current_value=0)
            p.save()


class ClientAccount(Model):

    user = OneToOneField(User, on_delete=CASCADE)

    def create_account(self):
        if MasterAccount.objects.filter(user=self.user).exists():
            return False
        if not ClientAccount.objects.filter(user=self.user).exists():
            p = ClientAccount(user=self.user)
            p.save()
