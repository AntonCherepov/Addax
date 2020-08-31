from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, \
    HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from rest_framework.views import APIView

from core.decorators import get_user_decorator
from core.utils import pagination
from feedbacks.forms import FeedBackForm
from feedbacks.models import FeedBack
from feedbacks.serializers import FeedBackSerializer, \
    FeedbackNotificationSerializer
from orders.constants import SUCCESSFULLY_COMPLETED, SELECTED
from orders.models import Order, Reply
from users.models import MasterAccount
from users.permissions import IsClient


class FeedBackView(APIView):

    def get(self, request):
        master_id = request.GET.get('master_id')
        master = get_object_or_404(MasterAccount, id=master_id)
        feedbacks = FeedBack.objects.filter(master=master)
        limit = request.GET.get('limit')
        offset = request.GET.get('offset')
        feedbacks, count = pagination(feedbacks, offset, limit)
        feedbacks = FeedBackSerializer(feedbacks, many=True)
        response_body = {
            'feedbacks': feedbacks.data,
            'count': count,
        }
        return Response(response_body, status=HTTP_200_OK)

    @get_user_decorator
    def post(self, request, user):
        if user.is_client() and not user.is_master():
            if master_id := request.POST.get('master_id'):
                form = FeedBackForm(request.POST)
                if form.is_valid():
                    try:
                        master = get_object_or_404(MasterAccount, id=master_id)
                    except ValueError:
                        return Response(
                            {'detail': 'master_id must be integer.'},
                            HTTP_400_BAD_REQUEST)
                    complete_orders = Order.objects.filter(
                        replies__master=master,
                        replies__status=SELECTED,
                        client=user.clientaccount)
                    feedbacks = FeedBack.objects.filter(
                        master=master,
                        client=user.clientaccount
                    )
                    if complete_orders and not feedbacks:
                        comment = request.POST.get('comment')
                        feedback = FeedBack.objects.create(
                            nickname=form.cleaned_data['nickname'],
                            comment=comment,
                            rating=form.cleaned_data['rating'],
                            master=master,
                            client=user.clientaccount
                        )
                        serialized = FeedBackSerializer(feedback)
                        return Response({'feedback': serialized.data},
                                        status=HTTP_201_CREATED)
                    else:
                        return Response(status=HTTP_400_BAD_REQUEST)
                else:
                    return Response(
                        {'detail': f'Form is not valid: {form.errors}'},
                        status=HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"detail": 'Field \'master_id\' not found.'},
                    status=HTTP_400_BAD_REQUEST)
        else:
            return Response(status=HTTP_403_FORBIDDEN)


class NotificationView(APIView):

    permission_classes = (IsClient,)

    @get_user_decorator
    def get(self, request, user):
        client = user.clientaccount

        complete_orders = Order.objects.filter(
            status=SUCCESSFULLY_COMPLETED,
            client=client)
        replies = Reply.objects.filter(status=SELECTED,
                                 order__in=complete_orders)
        # Here we getting only first completed
        # order replies between master and client
        replies = replies.order_by('master', 'id').distinct('master')
        masters_with_feedbacks = FeedBack.objects.filter(
                        client=client,
                        master__in=replies.values_list('master')
                        ).values_list('master')
        replies = replies.exclude(master__in=masters_with_feedbacks)
        serializer = FeedbackNotificationSerializer(replies, many=True)

        return Response({'feedbacks_notification_data': serializer.data},
                        status=HTTP_200_OK)
