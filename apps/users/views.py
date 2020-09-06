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

from core.decorators import get_user_decorator
from core.exceptions import RequestUserError
from core.utils import extract_exception_text
from users.constants import MASTER, CLIENT, USER_CONFIRMED, USER_REGISTERED
from manuals.models import MasterType
from users.permissions import IsConfirmed, IsNotBanned
from users.models import User, PhoneCode, MasterAccount, ClientAccount
from users.utils import get_token
from users.forms import RegistrationForm, ConfirmationForm
from users.serializers import (UserSerializer, MasterSerializer,
                               UserMasterSerializer, UserClientSerializer,
                               MasterAccountOwnerSerializer)


class RegistrationView(APIView):

    permission_classes = (IsNotBanned,)

    def post(self, request):
        registration_form = RegistrationForm(request.POST)
        random_code = str(randint(100000, 999999))
        if registration_form.is_valid():
            phone_number = registration_form.cleaned_data['phone']
            type_code = registration_form.cleaned_data['type_code']
            try:
                user = User(phone_number=phone_number, username=phone_number,
                            type_code=type_code)
                user.validate_registration_request()
                user.type_code = type_code
                user.status = USER_REGISTERED
                user.save()
            except ValidationError as e:
                e = extract_exception_text(e)
                if e == 'User with this phone_number already exists':
                    user = User.objects.get(phone_number=phone_number)
                    user.status = USER_REGISTERED
                    user.save()
                else:
                    return Response({'detail': e},
                                    status=HTTP_400_BAD_REQUEST)
            c = PhoneCode(user=user, code=random_code)
            c.save()
            return Response(status=HTTP_200_OK)
        else:
            return Response({'detail': f'Form is not valid: '
                                       f'{registration_form.errors}'},
                            status=HTTP_400_BAD_REQUEST)


class ConfirmationView(APIView):

    def post(self, request):
        confirmation_form = ConfirmationForm(request.POST)
        if confirmation_form.is_valid():
            phone_number = confirmation_form.cleaned_data['phone']
            code = confirmation_form.cleaned_data['code']
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
                content = {'token': token.key}
                return Response(content, status=HTTP_200_OK)

            except ValidationError as e:
                e = extract_exception_text(e)
                return Response({'detail': e}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': f'Form is not valid: '
                                       f'{confirmation_form.errors}'},
                            status=HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    permission_classes = (IsAuthenticated, IsConfirmed)

    def post(self, request):
        try:
            token = get_token(request)
            token.delete()
            return Response(status=HTTP_200_OK)
        except RequestUserError as e:
            return Response({'detail': str(e)}, status=HTTP_400_BAD_REQUEST)


class IsValidTokenView(APIView):

    permission_classes = (IsAuthenticated, IsConfirmed)

    @get_user_decorator
    def get(self, request, user):
        if user.is_master():
            master_exclude_fields = {
                'name', 'types', 'about_myself', 'address',
                'avatar_album_id', 'gallery_album_id', 'workplace_album_id',
            }
            serialized_user = UserMasterSerializer(user, context={
                'master_exclude_fields': master_exclude_fields
            })
        else:
            serialized_user = UserClientSerializer(user)
        content = {'user': serialized_user.data}
        return Response(content)


class MastersView(APIView):

    permission_classes = (IsConfirmed, IsNotBanned)

    @get_user_decorator
    def get(self, request, user, master_id):
        master = get_object_or_404(MasterAccount, id=master_id)
        if user.type_code == MASTER and user.masteraccount.id == master_id:
            serializer = MasterAccountOwnerSerializer(master)
        else:
            master_exclude_fields = {'status'}
            serializer = MasterSerializer(
                master,
                context={'request': request,
                         'user': user,
                         'master_id': master_id,
                         'master_exclude_fields': master_exclude_fields},
            )
        return Response(serializer.data, status=HTTP_200_OK)

    @get_user_decorator
    def patch(self, request, user, master_id):
        if user.is_master() and user.masteraccount.id == master_id:
            master = get_object_or_404(MasterAccount, id=master_id)
            try:
                if email := request.POST.get('email'):
                    master.user.email = email
                if name := request.POST.get('name'):
                    master.name = name
                if address := request.POST.get('address'):
                    master.address = address
                if about_myself := request.POST.get('about_myself'):
                    master.about_myself = about_myself
                if master_types := request.POST.get('master_types'):
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
                master.user.save()
            except (ObjectDoesNotExist, DataError, ValueError) as e:
                return Response({'detail': str(e)},
                                status=HTTP_400_BAD_REQUEST)
        else:
            return Response(status=HTTP_403_FORBIDDEN)
        serializer = MasterAccountOwnerSerializer(master)
        return Response({'master': serializer.data}, status=HTTP_200_OK)


class ClientsView(APIView):

    permission_classes = (IsAuthenticated,)

    @get_user_decorator
    def get(self, request, user, client_id):
        serialized_user = UserSerializer(user)
        content = {'message': 'User is authorized',
                   'user': serialized_user.data}
        return Response(content)
