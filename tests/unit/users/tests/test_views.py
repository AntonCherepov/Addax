from django.test import TestCase

from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APIClient

from manuals.models import MasterType, City

import json

#Testy pro silné...
class test_registration(TestCase): #класс, тестирую

    @classmethod
    def setUpTestData(cls): # один раз перед всеми методами
        city = City(name="Воронеж")
        city.save()
        MasterType.objects.bulk_create(
            [MasterType(name="Визажист"),
             MasterType(name="Косметолог"),
             MasterType(name="Массажист"),
             MasterType(name="Мастер по маникюру"),
             MasterType(name="Мастер по наращиванию ресниц"),
             MasterType(name="Парикмахер"),
             MasterType(name="Мастер эпиляции")])


    def setUp(self): #перед каждым методом
        call_command("loaddata", 'fixtures.json', verbosity=0)
        self.client = APIClient()
        self.url_registration = '/v1/users/registration/'


    def registration(self, phone, type):
        response = self.client.post(self.url_registration, {'phone' : phone, 'type_code' : type})
        return response

    def sub_test_success_registration(self, phone, type, message='success registration'):
        with self.subTest():
            response = self.registration(phone, type)
            self.assertEqual(response.status_code, status.HTTP_200_OK, 'error status ' + message)
            self.assertIsNone(response.data, 'not 0 length body response ' + message)

    def test_success_registration(self):
        self.sub_test_error_type('9000000001', 'c') #user with status 'rg'
        self.sub_test_error_type('9000000101', 'c')  #user with status 'cf'

        self.sub_test_error_type('9000001001', 'm') #user rg master uv
        self.sub_test_error_type('9000001101', 'm') #user cf master uv

    def sub_test_registration_user_bn(self, phone, type):
        with self.subTest():
            response = self.registration(phone, type)
            self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIsNotNone(response.data, 'not detail')
            response_json = json.loads(response.data)
            self.assertTrue(response_json['detail'], 'Этот номер забанен')

    #banned user
    def test_registration_user_bn(self):
        self.sub_test_registration_user_bn('9000000201', 'c') #user bn
        self.sub_test_registration_user_bn('9000001001', 'm') #user bn master uv

    def sub_test_registration_in_row(self, phone, type, size_row):
        with self.subTest():
            for i in range(0, size_row):
                response = self.registration(phone, type)
                self.assertEqual(response.status_code, status.HTTP_200_OK)

    #registration in a row
    def test_registration_in_row(self):
        self.sub_test_registration_in_row('9000000151', 'c', 4)
        self.sub_test_registration_in_row('9000001051', 'm', 4)

    def sub_test_error_type(self, phone, type):
        with self.subTest():
            error_detail = 'Ошибка во входных данных'
            response = self.registration(phone, type)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIsNotNone(response.data)
            json_parsed = response.data
            self.assertTrue('detail' in  json_parsed)
            self.assertEqual(json_parsed['detail'], error_detail)

    def test_registration_error_input_data(self):
        #error type
        self.sub_test_error_type('9000000150', 'q')
        self.sub_test_error_type('9000000151', 'cc')
        self.sub_test_error_type('9000000152', '1')
        self.sub_test_error_type('9000000152', '!=f')
        self.sub_test_error_type('9000000152', '.')
        self.sub_test_error_type('9000000152', 'с') #russian с

        #error phone
        self.sub_test_error_type('90000000010', 'с')
        self.sub_test_error_type('9', 'с')
        self.sub_test_error_type('900000000', 'с')
        self.sub_test_error_type('8000000000', 'с')
        self.sub_test_error_type('phonephone', 'с')
        self.sub_test_error_type('9honephone', 'с')


# class test_valid_user(TestCase):
#
#     @classmethod
#     def setUpTestData(cls): # один раз перед всеми методами
#         city = City(name="Воронеж")
#         city.save()
#         MasterType.objects.bulk_create(
#             [MasterType(name="Визажист"),
#              MasterType(name="Косметолог"),
#              MasterType(name="Массажист"),
#              MasterType(name="Мастер по маникюру"),
#              MasterType(name="Мастер по наращиванию ресниц"),
#              MasterType(name="Парикмахер"),
#              MasterType(name="Мастер эпиляции")])
#
#
#     def setUp(self): #перед каждым методом
#         call_command("loaddata", 'fixtures.json', verbosity=0)
#         self.client = APIClient()
#         self.url_validation = '/v1/users/'
#
#     def validation(self, token):
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)
#         response = self.client.get(self.url_validation)
#         return response
#
#     def sub_test_success_valid_client(self, token):
#         with self.subTest():
#             response = self.validation(token)
#             self.assertEqual(response.status_code, status.HTTP_200_OK)
#             self.assertIsNotNone(response.data)
#             json_parsed = json.loads()
#
#     def test_success_valid(self):






