import json
from random import randint

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import DataError
from rest_framework.generics import get_object_or_404

from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_403_FORBIDDEN)
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from users.constants import MASTER, CLIENT, USER_CONFIRMED, USER_REGISTERED
from manuals.models import MasterType
from users.permissions import IsConfirmed, IsNotBanned
from users.models import (User, PhoneCode, MasterAccount, ClientAccount)
from users.utils import get_token, get_user
from users.forms import RegistrationForm, ConfirmationForm
from users.serializers import UserSerializer, MasterSerializer, \
    UserMasterSerializer


class RegistrationView(APIView):

    permission_classes = (IsNotBanned,)

    def post(self, request):
        registration_form = RegistrationForm(request.POST)
        random_code = str(randint(100000, 999999))
        if registration_form.is_valid():
            phone_number = registration_form.cleaned_data["phone"]
            type_code = registration_form.cleaned_data["type_code"]
            try:
                user = User(phone_number=phone_number, username=phone_number,
                            type_code=type_code)
                user.validate_registration_request()
                user.type_code = type_code
                user.status = USER_REGISTERED
                user.save()
            except ValidationError as e:
                if str(e) == "['User with this phone_number already exists']":
                    user = User.objects.get(phone_number=phone_number)
                    user.status = USER_REGISTERED
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
                user.status = USER_CONFIRMED
                user.save()
                if user.type_code == MASTER:
                    MasterAccount(user=user).create_account()
                elif user.type_code == CLIENT:
                    ClientAccount(user=user).create_account()
                try:
                    token = Token.objects.get(user=user)
                except ObjectDoesNotExist:
                    token = Token.objects.create(user=user)
                content = {"token": token.key}
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
        if u.is_master():
            master_exclude_fields = {
                "name", "types", "about_myself", "address",
                "avatar_album_id", "gallery_album_id", "workplace_album_id",
            }
            serialized_user = UserMasterSerializer(u, context={
                "master_exclude_fields": master_exclude_fields
            })
        else:
            serialized_user = UserSerializer(u)
        content = {"user": serialized_user.data}
        return Response(content)


class MastersView(APIView):

    permission_classes = (IsConfirmed, IsNotBanned)

    def get(self, request, master_id):
        user = get_user(request)
        master = get_object_or_404(MasterAccount, id=master_id)
        master_exclude_fields = {"status"}
        if user.type_code == MASTER:
            if user.masteraccount.id == master_id:
                master_exclude_fields.remove("status")
        serializer = MasterSerializer(
            master,
            context={"request": request,
                     "user": user,
                     "master_id": master_id,
                     "master_exclude_fields": master_exclude_fields},
        )
        return Response(serializer.data, status=HTTP_200_OK)

    def patch(self, request, master_id):
        user = get_user(request)
        if user.is_master() and user.masteraccount.id == master_id:
            master = get_object_or_404(MasterAccount, id=master_id)
            name = request.POST.get('name')
            address = request.POST.get('address')
            about_myself = request.POST.get('about_myself')
            master_types = request.POST.get('master_types')
            try:
                if name:
                    master.name = name
                if address:
                    master.address = address
                if about_myself:
                    master.about_myself = about_myself
                if master_types:
                    master_types = set(json.loads(master_types))
                    master_types = [
                        MasterType.objects.get(id=int(t))
                        for t
                        in master_types
                                    ]
                    master.save()
                    master.types.clear()
                    master.types.add(*master_types)
                else:
                    master.save()
            except (ObjectDoesNotExist, DataError, ValueError):
                return Response(status=HTTP_400_BAD_REQUEST)
        else:
            return Response(status=HTTP_403_FORBIDDEN)
        serializer = MasterSerializer(master)
        return Response({"master": serializer.data}, status=HTTP_200_OK)


class ClientsView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, client_id):
        u = get_user(request)
        serialized_user = UserSerializer(u)
        content = {"message": "User is authorized",
                   "user": serialized_user.data}
        return Response(content)
