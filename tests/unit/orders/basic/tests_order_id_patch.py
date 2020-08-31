from datetime import datetime as dt, timedelta

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from manuals.models import City, MasterType
from orders.constants import (SELECTION_OF_MASTERS, CONSIDERED, SELECTED,
                              CANCELED_BY_MASTER, MASTER_SELECTED,
                              CANCELED_BY_CLIENT)
from users.constants import CLIENT, MASTER, USER_CONFIRMED
from users.models import MasterAccount, User, ClientAccount
from orders.models import Order, Reply


class OrderUpdateTestCase(APITestCase):

    def setUp(self):
        # Create test datetime objects
        current_dt = dt.now()
        date_from = current_dt + timedelta(days=1)
        date_to = current_dt + timedelta(days=2)

        # Create test users
        # Client
        self.main_client = User.objects.create(phone_number='9000000000',
                                       username='9000000000',
                                       type_code=CLIENT,
                                       status=USER_CONFIRMED)
        ClientAccount(user=self.main_client).create_account()
        self.main_client_token = Token.objects.create(user=self.main_client)
        # Master 1
        master_1 = User.objects.create(phone_number='9000000001',
                                       username='9000000001',
                                       type_code=MASTER,
                                       status=USER_CONFIRMED)
        MasterAccount(user=master_1).create_account()
        self.master_1_token = Token.objects.create(user=master_1)
        # Master 2
        master_2 = User.objects.create(phone_number='9000000002',
                                       username='9000000002',
                                       type_code=MASTER,
                                       status=USER_CONFIRMED)
        MasterAccount(user=master_2).create_account()
        self.master_2_token = Token.objects.create(user=master_2)

        # Create test manuals
        city = City(name='Воронеж')
        city.save()
        MasterType.objects.bulk_create(
            [MasterType(name='Визажист'),
             MasterType(name='Косметолог'),
             MasterType(name='Массажист'),
             MasterType(name='Мастер по маникюру'),
             MasterType(name='Мастер по наращиванию ресниц'),
             MasterType(name='Парикмахер'),
             MasterType(name='Мастер эпиляции')])
        default_master_type = MasterType.objects.get(name='Визажист')

        # Create test order and order replies
        order_ms = Order(
            id=1,
            client=self.main_client.clientaccount,
            city=city,
            master_type=default_master_type,
            request_date_from=date_from,
            request_date_to=date_to,
            status=MASTER_SELECTED,
            description=None,
        )
        order_ms.create_album()
        order_ms.save()
        order_sm = Order(
            id=2,
            client=self.main_client.clientaccount,
            city=city,
            master_type=default_master_type,
            request_date_from=date_from,
            request_date_to=date_to,
            status=SELECTION_OF_MASTERS,
            description=None,
        )
        order_sm.create_album()
        order_sm.save()
        # Default Order for Reply is order_ms
        self.reply_considered = Reply.objects.create(
            id=1,
            cost=100,
            suggested_time_to=date_from,
            suggested_time_from=date_to,
            master=master_1.masteraccount,
            order=order_ms,
            comment='',
            status=CONSIDERED
        )
        self.reply_selected = Reply.objects.create(
            id=2,
            cost=200,
            suggested_time_to=date_from,
            suggested_time_from=date_to,
            master=master_2.masteraccount,
            order=order_ms,
            comment='',
            status=SELECTED
        )
        self.order_sm_reply_considered = Reply.objects.create(
            id=3,
            cost=200,
            suggested_time_to=date_from,
            suggested_time_from=date_to,
            master=master_2.masteraccount,
            order=order_sm,
            comment='',
            status=CONSIDERED
        )

    def test_cancel_by_master(self):
        """SubCase 2"""
        order = Order.objects.get(client=self.main_client.clientaccount,
                                  status=MASTER_SELECTED)
        data = {'status_code': 'cm'}
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' +
                                              str(self.master_2_token))
        response = client.patch('/v1/orders/1/', data)
        order_after_request = Order.objects.get(id=order.id)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(order_after_request.status,
                         CANCELED_BY_MASTER)

    def test_cancel_by_wrong_master(self):
        """SubCase 2 security test 1"""
        order = Order.objects.get(client=self.main_client.clientaccount,
                                  status=MASTER_SELECTED)
        data = {'status_code': 'cm'}
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' +
                                              str(self.master_1_token))

        response = client.patch('/v1/orders/1/', data)
        order_after_request = Order.objects.get(id=order.id)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(order_after_request.status,
                         MASTER_SELECTED)

    def test_cancel_ms_by_client(self):
        """SubCase 1"""
        order = Order.objects.get(
            id=1,
            client=self.main_client.clientaccount,
            status=MASTER_SELECTED
        )
        data = {'status_code': 'cc'}
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' +
                                              str(self.main_client_token))

        response = client.patch('/v1/orders/1/', data)
        order_after_request = Order.objects.get(id=order.id)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(order_after_request.status,
                         CANCELED_BY_CLIENT)

    def test_cancel_sm_by_client(self):
        """SubCase 1"""
        order = Order.objects.get(
            id=2,
            client=self.main_client.clientaccount,
            status=SELECTION_OF_MASTERS
        )
        data = {'status_code': 'cc'}
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' +
                                              str(self.main_client_token))
        response = client.patch('/v1/orders/2/', data)
        order_after_request = Order.objects.get(id=order.id)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(order_after_request.status,
                         CANCELED_BY_CLIENT)

    def test_master_select_by_client(self):
        """SubCase 3"""
        order = Order.objects.get(
            id=2,
            client=self.main_client.clientaccount,
            status=SELECTION_OF_MASTERS
        )
        data = {
            'status_code': 'ms',
            'reply_id': str(self.order_sm_reply_considered.id)
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' +
                                              str(self.main_client_token))

        response = client.patch('/v1/orders/2/', data)
        order_after_request = Order.objects.get(id=order.id)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(order_after_request.status,
                         MASTER_SELECTED)
