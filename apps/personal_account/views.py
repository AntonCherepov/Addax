from random import randint

from django.utils import timezone
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from personal_account.smsc_api import SMSC
from personal_account.models import User, PhoneCode
from personal_account.serializers import UserSerializer


def default(request):
    return HttpResponse("Default")


class Registration(APIView):

    @staticmethod
    def post(request):
        phone = str(request.data["phone"])
        # if re.match(r"(\+7)|8|7\d{10}", phone):
        # sms = SMSC()
        random_code = str(randint(100000, 999999))
        try:
            u = User.objects.get(phone_number=phone[-10::])
        except ObjectDoesNotExist:
            u = User(phone_number=phone[-10::],
                     username=random_code + "U",
                     is_active=False)
            u.save()
        c = PhoneCode(user_id=u.id, code=random_code)
        c.save()
        print(random_code)
        # sms.send_sms("7"+phone,
        #              f"Ваш кот еще спит: {random_code}",
        #              sender="sms")

        return Response({"message": random_code})

    @staticmethod
    def get(request):
        active_users = User.objects.filter(is_active=True)
        inactive_users = User.objects.filter(is_active=False)
        serializer_active = UserSerializer(active_users, many=True)
        serializer_inactive = UserSerializer(inactive_users, many=True)
        return Response({"message":
                        {"active_users": serializer_active.data,
                         "inactive_users": serializer_inactive.data}
                         })


class Confirmation(APIView):

    @staticmethod
    def post(request):
        phone = str(request.data["phone"])
        code = str(request.data["code"])
        try:
            u = User.objects.get(phone_number=phone[-10::])
            confirm_code = PhoneCode.objects.filter(user_id=u.id) \
                                            .order_by("-id")[:1:][0]
        except ObjectDoesNotExist:
            return Response({"message": "No User or Code"})

        time_difference = timezone.now() - confirm_code.query_time
        if int(code) != confirm_code.code:
            content = {"message": "Incorrect code"}
        elif time_difference.seconds > 300:
            content = {"message": "Code is too old"}
        else:
            u.is_active = True
            u.save()
            try:
                token = Token.objects.get(user=u)
            except ObjectDoesNotExist:
                token = Token.objects.create(user=u)
            content = {"message": "User is active", "token": token.key}
        return Response(content)

    @staticmethod
    def get(request):
        return Response({"message": "No GET for this url"}, status=405)


class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        try:
            auth_header = request.META["HTTP_AUTHORIZATION"].split(" ")
            token_raw = auth_header[1]
            t = Token.objects.get(key=token_raw)
            t.delete()
            content = {"message":
                       f"Logout success for user id = {t.user_id}"}
        except ObjectDoesNotExist:
            content = {"message": "No login"}
        return Response(content)

    @staticmethod
    def get(request):
        content = {"message": "User is authorized"}
        return Response(content)
