from distutils.util import strtobool

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.utils.datetime_safe import datetime as dt
from django.core.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_201_CREATED, HTTP_403_FORBIDDEN)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from albums.utils import save_photos
from core.utils import pagination, string_to_set
from manuals.models import MasterType, City
from orders.forms import OrderForm, ReplyForm
from orders.serializers import OrderSerializer, ReplySerializer
from users.permissions import IsConfirmed, MasterReadOnly
from users.models import MasterAccount
from users.utils import get_user
from orders.models import Order, Reply
from orders.utils import (order_by_id, get_orders_and_master_for_user,
                          get_order_by_id_and_master_for_user)
from orders.constants import (SUCCESSFULLY_COMPLETED, SELECTION_OF_MASTERS,
                              MASTER_SELECTED, CANCELED_BY_CLIENT,
                              CANCELED_BY_MASTER, CLIENT_DID_NOT_ARRIVE,
                              CONSIDERED, REJECTED,
                              SELECTED)


class OrderView(APIView):
    """Implementation of interaction with client orders."""

    permission_classes = (IsAuthenticated, IsConfirmed, MasterReadOnly)

    def post(self, request):
        """
        Creates a order for work by the master. Creation of
        orders is not available for users with a master account.
        """
        user = get_user(request)
        if isinstance(user, dict):
            return Response(status=HTTP_400_BAD_REQUEST)
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            city = City.objects.get(id=order_form.cleaned_data['city_id'])
            master_type_id = MasterType.objects.get(
                id=order_form.cleaned_data['master_type_id'])
            status = SELECTION_OF_MASTERS
            request_date_from = dt.utcfromtimestamp(
                order_form.cleaned_data['request_date_from'])
            request_date_to = dt.utcfromtimestamp(
                order_form.cleaned_data['request_date_to'])
            description = request.POST.get('description')
            order = Order(
                client=user.clientaccount,
                city=city,
                master_type=master_type_id,
                request_date_from=request_date_from,
                request_date_to=request_date_to,
                status=status,
                description=description,
            )
            try:
                order.validate()
                order.create_album()
                order.save()
                # Add uploaded photos to albums
                files = request.FILES
                if files:
                    order.album.validate_post_request(user=user, files=files)
                    save_photos(files=files, user=user, album=order.album)
                order.album.is_closed = True
                order.album.save()
            except ValidationError:
                return Response(status=HTTP_400_BAD_REQUEST)
            order = OrderSerializer(order)
            return Response({"order": order.data}, status=HTTP_201_CREATED)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        Returns (filtered) JSON-serialized orders with selected fields.
        A set of fields may contain nested replies objects. Available
        order objects and set of fields depends on user permissions.
        """
        user = get_user(request)
        if isinstance(user, dict):
            return Response(user)

        order_exclude_fields = set()
        master_exclude_fields = {'status'}
        limit = request.GET.get("limit")
        offset = request.GET.get("offset")
        order_status = request.GET.get("order_status")
        exist_master_reply = request.GET.get("exist_master_reply")

        # Extract all possible order objects for the current user
        orders, master = get_orders_and_master_for_user(
            request=request,
            user=user,
            order_exclude_fields=order_exclude_fields
        )
        # Filter extracted orders
        try:
            if order_status:
                orders = orders.filter(
                    status__in=string_to_set(order_status)
                )
            if exist_master_reply is not None:
                exist_master_reply = not strtobool(exist_master_reply)
                orders = orders.filter(replies__isnull=exist_master_reply)
            orders, orders_count = pagination(
                objects=orders,
                offset=offset,
                limit=limit
            )
        except (ValueError, OSError):
            return Response(status=HTTP_400_BAD_REQUEST)
        except AssertionError as e:
            if str(e) == "Negative indexing is not supported.":
                return Response(status=HTTP_400_BAD_REQUEST)
        orders = OrderSerializer(
            orders,
            many=True,
            context={
                'request': request,
                'order_exclude_fields': order_exclude_fields,
                'master_exclude_fields': master_exclude_fields,
                'master': master,
             },
                                 )
        try:
            return Response({"orders": orders.data, "count": orders_count},
                            status=HTTP_200_OK)
        except IntegrityError:
            return Response(status=HTTP_400_BAD_REQUEST)


class OrderByIdView(APIView):
    """Implementation of interaction with client order taken by id."""

    def patch(self, request, order_id):
        user = get_user(request)
        order = get_object_or_404(Order, id=order_id)
        try:
            selected_master = order.replies.get(status=SELECTED).master
        except ObjectDoesNotExist:
            selected_master = None
        order_exclude_fields = {"replies_count"}
        status_code = request.POST.get("status_code")
        selection_date = request.POST.get("selection_date")
        reply_id = request.POST.get("reply_id")
        try:
            if status_code:
                if user.is_client() and order.client == user.clientaccount:
                    if (status_code == MASTER_SELECTED and
                            order.status == SELECTION_OF_MASTERS and
                            reply_id):
                        reply = order.get_reply_by_id(reply_id)
                        reply.status = SELECTED
                        order.status = MASTER_SELECTED
                        rejected_replies = order.replies.exclude(id=reply_id)
                        rejected_replies.update(status=REJECTED)
                        reply.save()
                    elif (status_code == CANCELED_BY_CLIENT and
                          order.status in [SELECTION_OF_MASTERS,
                                           MASTER_SELECTED]):
                        order.status = CANCELED_BY_CLIENT
                    else:
                        return Response(status=HTTP_400_BAD_REQUEST)
                elif (user.is_master() and
                      user.masteraccount == selected_master):
                    possible_statuses = [
                        CANCELED_BY_MASTER,
                        CLIENT_DID_NOT_ARRIVE,
                        SUCCESSFULLY_COMPLETED,
                                         ]
                    if (order.status == MASTER_SELECTED and
                            status_code in possible_statuses):
                        order.status = status_code
                    else:
                        return Response(status=HTTP_400_BAD_REQUEST)
                else:
                    return Response(status=HTTP_403_FORBIDDEN)
            if selection_date:
                if user.is_master():
                    if user.masteraccount != selected_master:
                        return Response(status=HTTP_403_FORBIDDEN)
                order.update_selection_date(selection_date)
        except ValidationError:
            return Response(status=HTTP_400_BAD_REQUEST)
        order.save()
        serialized_order = OrderSerializer(order, context={
            "order_exclude_fields": order_exclude_fields
        })
        return Response({"order": serialized_order.data}, status=HTTP_200_OK)

    def get(self, request, order_id):
        user = get_user(request)
        if isinstance(user, dict):
            return Response(user)

        master_exclude_fields = {'status'}
        order_exclude_fields = set()
        try:
            order, master = get_order_by_id_and_master_for_user(
                request=request,
                user=user,
                order_exclude_fields=order_exclude_fields,
                order_id=order_id
            )
        except ValidationError:
            return Response(status=HTTP_400_BAD_REQUEST)
        order = OrderSerializer(
            order,
            context={
                'request': request,
                'order_exclude_fields': order_exclude_fields,
                'master_exclude_fields': master_exclude_fields,
                'master': master,
            },
        )

        return Response({"order": order.data}, status=HTTP_200_OK)


class RepliesView(APIView):
    """
    Implementation of interaction with
    master replies taken by order id.
    """

    permission_classes = (IsAuthenticated, IsConfirmed)

    def post(self, request, order_id):
        user = get_user(request)
        try:
            master = MasterAccount.objects.get(user=user)
        except ObjectDoesNotExist:
            return Response(status=HTTP_403_FORBIDDEN)
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            try:
                order = order_by_id(order_id)
                suggested_time_from = dt.utcfromtimestamp(
                    reply_form.cleaned_data['suggested_time_from'])
                suggested_time_to = dt.utcfromtimestamp(
                    reply_form.cleaned_data['suggested_time_to'])
                reply = Reply(
                    cost=reply_form.cleaned_data['cost'],
                    suggested_time_to=suggested_time_to,
                    suggested_time_from=suggested_time_from,
                    master=master,
                    order=order,
                    comment=request.POST.get('comment'),
                    status=CONSIDERED
                )
                reply.validate()
            except ValidationError:
                return Response(status=HTTP_400_BAD_REQUEST)
            reply.save()
            reply = ReplySerializer(reply)
            return Response({"reply": reply.data}, status=HTTP_201_CREATED)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)

    def get(self, request, order_id):
        user = get_user(request)
        master_exclude_fields = {'status'}
        try:
            order, master = get_order_by_id_and_master_for_user(
                request=request,
                user=user,
                order_exclude_fields=set(),
                order_id=order_id
            )
        except ValidationError:
            return Response(status=HTTP_400_BAD_REQUEST)
        if user.is_master():
            replies = order.replies.filter(master=master)
        else:
            replies = order.replies
        replies = ReplySerializer(
            replies,
            many=True,
            context={
                'request': request,
                'master_exclude_fields': master_exclude_fields,
            },
        )
        context = {
            "order_id": order.id,
            "replies": replies.data,
                   }
        return Response(context, status=HTTP_200_OK)
