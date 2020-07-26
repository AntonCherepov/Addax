from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, \
    HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN
from rest_framework.views import APIView

from core.decorators import get_user_decorator
from core.utils import pagination
from feedbacks.forms import FeedBackForm
from feedbacks.models import FeedBack
from feedbacks.serializers import FeedBackSerializer
from orders.constants import SUCCESSFULLY_COMPLETED, SELECTED
from orders.models import Order, Reply
from users.models import MasterAccount
from users.serializers import MasterSerializer


class FeedBackView(APIView):

    def get(self, request, master_id):
        master = get_object_or_404(MasterAccount, id=master_id)
        feedbacks  = FeedBack.objects.filter(master=master)
        if feedbacks:
            limit = request.GET.get("limit")
            offset = request.GET.get("offset")
            feedbacks, count = pagination(feedbacks, offset, limit)
            feedbacks = FeedBackSerializer(feedbacks, many=True)
            response_body = {
                "feedbacks": feedbacks.data,
                "count": count,
            }
            return Response(response_body, status=HTTP_200_OK)
        else:
            return Response(status=HTTP_404_NOT_FOUND)

    @get_user_decorator
    def post(self, request, user, master_id):
        if user.is_client() and not user.is_master():
            form = FeedBackForm(request.POST)
            if form.is_valid():
                master = get_object_or_404(MasterAccount, id=master_id)
                complete_orders = Order.objects.filter(
                    replies__master=master,
                    replies__status=SUCCESSFULLY_COMPLETED,
                    client=user.clientaccount)
                feedbacks = FeedBack.objects.filter(master=master,
                                                    client=user.clientaccount)
                if complete_orders and not feedbacks:
                    comment = request.POST.get("comment")
                    feedback = FeedBack.objects.create(
                        nickname=form.cleaned_data["nickname"],
                        comment=comment,
                        rating=form.cleaned_data["rating"],
                        master=master,
                        client=user.clientaccount
                    )
                    serialized = FeedBackSerializer(feedback)
                    return Response({"feedback": serialized.data},
                                    status=HTTP_201_CREATED)
                else:
                    return Response(status=HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {"detail": f"Form is not valid: {form.errors}"},
                    status=HTTP_400_BAD_REQUEST
                )


class NotificationView(APIView):

    @get_user_decorator
    def get(self, request, user):
        master_exclude_fields = ("types", "status",
                                 "gallery_album_id", "workplace_album_id")
        if user.is_client():
            client = user.clientaccount
            complete_orders = Order.objects.filter(
                status=SUCCESSFULLY_COMPLETED,
                client=client)
            cs_masters = Reply.objects.filter(
                status=SELECTED,
                order__in=complete_orders).values_list("master")
            masters_with_feedbacks = FeedBack.objects.filter(
                client=client,
                master__in=cs_masters).values_list("master")
            masters_id = cs_masters.difference(masters_with_feedbacks)
            # masters_without_feedbacks
            masters = MasterAccount.objects.filter(id__in=masters_id)
            serializer = MasterSerializer(
                masters,
                many=True,
                context={"master_exclude_fields": master_exclude_fields},
            )
            return Response({"feedbacks": serializer.data}, status=HTTP_200_OK)
        return Response(status=HTTP_403_FORBIDDEN)
