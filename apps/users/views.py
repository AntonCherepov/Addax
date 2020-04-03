from random import randint

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework.generics import get_object_or_404

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from config.constants import DEFAULT_MASTER_FIELDS
from manuals.models import UserStatus
from users.permissions import IsConfirmed, IsNotBanned
from users.models import (User, PhoneCode, UserType, MasterAccount,
                          ClientAccount)
from users.utils import get_token, get_user
from users.forms import RegistrationForm, ConfirmationForm
from users.serializers import UserSerializer, MasterSerializer


class RegistrationView(APIView):

    permission_classes = (IsNotBanned,)

    def post(self, request):
        registration_form = RegistrationForm(request.POST)
        random_code = str(randint(100000, 999999))
        if registration_form.is_valid():
            phone_number = registration_form.cleaned_data["phone"]
            type_code = registration_form.cleaned_data["type_code"]
            try:
                user = User(phone_number=phone_number, username=phone_number)
                user.validate_registration_request(type_code)
                user.type_code = UserType.objects.get(code=type_code)
                user.status_code = UserStatus.objects.get(code="rg")
                user.save()
            except ValidationError as e:
                if str(e) == "['User with this phone_number already exists']":
                    user = User.objects.get(phone_number=phone_number)
                    user.status_code = UserStatus.objects.get(code="rg")
                    user.save()
                else:
                    return Response(status=HTTP_400_BAD_REQUEST)
            c = PhoneCode(user=user, code=random_code)
            c.save()
            return Response(status=HTTP_200_OK)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)


class ConfirmationView(APIView):

    def post(self, request):
        confirmation_form = ConfirmationForm(request.POST)
        if confirmation_form.is_valid():
            phone_number = confirmation_form.cleaned_data["phone"]
            code = confirmation_form.cleaned_data["code"]
            try:
                user = User.objects.get(phone_number=phone_number)
                user.validate_confirmation_request()
                PhoneCode(user=user, code=code).validate()
                user.status_code = UserStatus.objects.get(code="cf")
                user.save()
                if user.type_code.code == "m":
                    MasterAccount(user=user).create_account()
                elif user.type_code.code == "c":
                    ClientAccount(user=user).create_account()
                try:
                    token = Token.objects.get(user=user)
                except ObjectDoesNotExist:
                    token = Token.objects.create(user=user)
                content = {"token": token.key}
                # Авторизация с 2-ух устройств
                return Response(content, status=HTTP_200_OK)

            except ValidationError as e:
                return Response(status=HTTP_400_BAD_REQUEST)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    permission_classes = (IsAuthenticated, IsConfirmed)

    def post(self, request):
        token = get_token(request)
        if isinstance(token, dict):
            return Response(token)
        token.delete()
        return Response(status=HTTP_200_OK)


class IsValidTokenView(APIView):

    permission_classes = (IsAuthenticated, IsConfirmed)

    def get(self, request):
        u = get_user(request)
        serialized_user = UserSerializer(u)
        content = {"user": serialized_user.data}
        return Response(content)


class MastersView(APIView):

    permission_classes = (IsConfirmed, IsNotBanned)

    def get(self, request, master_id):
        u = get_user(request)
        master = get_object_or_404(MasterAccount, id=master_id)
        fields = request.GET.get("fields")
        exclude_fields = {"status"}
        if not fields:
            fields = DEFAULT_MASTER_FIELDS.copy()
        if u.type_code.name == "master":
            if u.masteraccount.id == master_id:
                exclude_fields.discard("status")
        serializer = MasterSerializer(master,
                                      fields=fields,
                                      exclude_fields=exclude_fields)
        return Response(serializer.data, status=HTTP_200_OK)

    def patch(self, request, master_id):
        content = {"id": master_id,
                   "name": "Салон",
                   "phone": 9101231232,
                   "address": "Вильгельма пика 4",
                   "about_myself": "Нет описания",
                   "master_types": ["Парикмахер", "Педикюр", "Маникюр"],
                   "status": "active",
                   "avatar": ["/media/avatar.jpg", "/media/avatar_small.jpg"],
                   "gallery": [["/media/lol.jpg", "/media/lol_small.jpg"],
                               ["/media/abc.jpg", "/media/abc_small.jpg"]
                               ]
                   }
        return Response(content, status=HTTP_200_OK)


class ClientsView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, client_id):
        u = get_user(request)
        serialized_user = UserSerializer(u)
        content = {"message": "User is authorized",
                   "user": serialized_user.data}
        return Response(content)
