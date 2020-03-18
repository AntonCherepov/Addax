from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import (CharField, Model, CASCADE,
                              IntegerField, DateTimeField, ForeignKey,
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
    if isinstance(t, Token):
        u = user_by_token(t)
        return u
    return


class User(AbstractUser):
    """ Модель для пользователей """

    phone_number = CharField('Номер', null=True, max_length=10, unique=True)
    type_code = ForeignKey(UserType, on_delete=SET_NULL, null=True)
    status_code = ForeignKey(UserStatus, on_delete=SET_NULL, null=True)
    date_modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number

    def is_banned(self):
        banned_status = UserStatus.objects.get(code="bn")
        return True if self.status_code == banned_status else False

    def is_confirmed(self):
        confirmed_status = UserStatus.objects.get(code="cf")
        return True if self.status_code == confirmed_status else False

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

    @staticmethod
    def validate_type_code(type_code):
        if not UserType.objects.filter(code=type_code).exists():
            raise ValidationError('Incorrect type_code')

    def validate_confirmation_request(self):
        users = User.objects.filter(phone_number=self.phone_number)
        if users.count() > 1:
            raise ValidationError('Too many users')
        elif not users.exists():
            raise ValidationError('User with this phone_number does not '
                                  'exists')
        elif self.status_code != UserStatus.objects.get(code="rg"):
            raise ValidationError("User does not need confirmation")

    def validate_registration_request(self, type_code):
        self.validate_phone()
        self.validate_type_code(type_code)

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
    type_s = ManyToManyField(MasterType, related_name="type")
    about_myself = CharField(null=True, max_length=10000)
    status_code = ForeignKey(MasterStatus, on_delete=SET_NULL, null=True)
    name = CharField(max_length=100)
    address = CharField(max_length=250)

    def create_account(self):
        if ClientAccount.objects.filter(user=self.user).exists():
            return False
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
        if MasterAccount.objects.filter(user=self.user).exists():
            return False
        if not ClientAccount.objects.filter(user=self.user).exists():
            p = ClientAccount(user=self.user)
            p.save()
