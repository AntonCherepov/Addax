from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import (ImageField, CharField, Model,
                              IntegerField, DateTimeField, ForeignKey, CASCADE,
                              OneToOneField, SET_NULL, ManyToManyField,)

from rest_framework.authtoken.models import Token

from manuals.models import MasterType, UserType, UserStatus, MasterStatus


def get_token(request):
    try:
        token_raw = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
        token = Token.objects.get(key=token_raw)
    except ObjectDoesNotExist:
        return {"message": "ObjectDoesNotExist::Token", "status": False}
    except KeyError:
        return {"message": "KeyError::HTTP_AUTHORIZATION", "status": False}
    return token


def user_by_token(token):
    try:
        user = User.objects.get(id=token.user_id)
    except ObjectDoesNotExist:
        return {"message": "ObjectDoesNotExist::User", "status": False}
    return user


def get_user(request):
    t = get_token(request)
    u = user_by_token(t)
    return u


class User(AbstractUser):
    """ Модель для пользователей """

    phone_number = CharField('Номер', null=True, max_length=10, unique=True)
    image = ImageField('Аватар', upload_to='UserAvatars', null=True)
    type_code = ForeignKey(UserType, on_delete=SET_NULL, null=True)
    status_code = ForeignKey(UserStatus, on_delete=SET_NULL, null=True)
    date_modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number

    def reg_validation(self, type_code=None):
        try:
            int(str(self.phone_number))
        except ValueError:
            raise ValidationError('phone_number is not a number')
        if str(self.phone_number)[0] != "9":
            raise ValidationError('Incorrect phone_number')
        if User.objects.filter(phone_number=self.phone_number).exists():
            raise ValidationError('User with this phone_number already exists')
        if type_code is not None:
            if not UserType.objects.filter(code=type_code).exists():
                raise ValidationError('Incorrect type_code')

    def confirm_validation(self):
        users = User.objects.filter(phone_number=self.phone_number)
        if users.count() > 1:
            raise ValidationError('Too many users')
        if not users.exists():
            raise ValidationError('User with this phone_number does not '
                                  'exists')
        else:
            return users[0]

    def activate(self):
        self.is_active = True
        self.save()

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

    def check_(self):
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
    type_s = ManyToManyField(MasterType, related_name="type")
    about_myself = CharField(default="Нет описания", max_length=10000)
    status_code = ForeignKey(MasterStatus, on_delete=SET_NULL, null=True)
    name = CharField(max_length=100)
    address = CharField(max_length=250)

    def create_account(self):
        if not MasterAccount.objects.filter(user=self.user).exists():
            try:
                status_code = MasterStatus.objects.get(code="uv")
            except ObjectDoesNotExist:
                status_code = MasterStatus(code="uv", name="unverified")
                status_code.save()
            p = MasterAccount(user=self.user, status_code=status_code)
            p.save()


class ClientAccount(Model):

    user = OneToOneField(User, on_delete=CASCADE)

    def create_account(self):
        if not ClientAccount.objects.filter(user=self.user).exists():
            p = ClientAccount(user=self.user)
            p.save()
