from django.test import TestCase

from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APIClient

from tests.unit.users.tests import Server
from tests.unit.users.tests.FactoryEnvironment import FactoryEnvironment
from tests.unit.users.tests.WrapperJsonValidation import WrapperJsonValidation

#Testy pro silné...
class test_user_registration_get(TestCase): #класс, тестирую

    detail_registration_user_banned = 'user banned'
    detail_registration_error_input_parameters = 'error input parameters'

    def setUp(self): #перед каждым методом
        call_command('flush', verbosity=0) #сбросить текущую бд
        #call_command("loaddata", 'fixtures.json', verbosity=0)
        call_command("loaddata", 'init_fixtures.json', verbosity=0)

    def registration(self, phone, type_code):
        response = Server.registration(phone, type_code)
        return response

    def sub_test_success_registration(self, phone, type, message='"success registration"'):
        with self.subTest():
            response = self.registration(phone, type)
            self.assertEqual(response.status_code, status.HTTP_200_OK, 'error status ' + message)
            self.assertIsNone(response.data, 'not 0 length body response ' + message)

    def test_success_registration(self):
        self.sub_test_success_registration(self.factory_user.get_phone('c', 1,'rg'), 'c')
        self.sub_test_success_registration(self.factory_user.get_phone('c', 2,'rg'), 'c')
        self.sub_test_success_registration(self.factory_user.get_phone('c', 10,'rg'), 'c')
        self.sub_test_success_registration(self.factory_user.get_phone('c', 12,'cf'), 'c')
        self.sub_test_success_registration(self.factory_user.get_phone('c', 23,'cf'), 'c')
        self.sub_test_success_registration(self.factory_user.get_phone('c', 72,'cf'), 'c')
        self.sub_test_success_registration(self.factory_user.get_phone('c', 101), 'c')
        self.sub_test_success_registration(self.factory_user.get_phone('c', 103), 'c')

        self.sub_test_success_registration(self.factory_user.get_phone('m', 1, 'rg', 'uv'), 'm')
        self.sub_test_success_registration(self.factory_user.get_phone('m', 1, 'cf', 'uv'), 'm')
        self.sub_test_success_registration(self.factory_user.get_phone('m', 1, 'rg', 'vr'), 'm')
        self.sub_test_success_registration(self.factory_user.get_phone('m', 1, 'cf', 'vr'), 'm')
        self.sub_test_success_registration(self.factory_user.get_phone('m', 1, 'cf', 'vr'), 'm')
        self.sub_test_success_registration(self.factory_user.get_phone('m', 1), 'm')
        self.sub_test_success_registration(self.factory_user.get_phone('m', 5), 'm')

    def sub_test_registration_user_bn(self, phone, type, message='"user banned"'):
        with self.subTest():
            response = self.registration(phone, type)
            self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST, 'error status ' + message)
            self.assertIsNotNone(response.data, 'not detail ' + message)
            self.assertTrue(self.validater.validate_error(response.data, self.detail_registration_user_banned),
                            'error detail ' + message)

    def test_registration_user_bn(self):
        self.sub_test_registration_user_bn(self.factory_user.get_phone('c', 1, 'bn'), 'c')
        self.sub_test_registration_user_bn(self.factory_user.get_phone('c', 10, 'bn'), 'c')
        self.sub_test_registration_user_bn(self.factory_user.get_phone('m', 1, 'bn', 'uv'), 'm')
        self.sub_test_registration_user_bn(self.factory_user.get_phone('m', 1, 'bn', 'vr'), 'm')
        self.sub_test_registration_user_bn(self.factory_user.get_phone('m', 1, 'bn', 'bn'), 'm')

    def sub_test_registration_in_row(self, phone, type, size_row, message = '"registration in row"'):
        with self.subTest():
            for i in range(0, size_row):
                self.sub_test_success_registration(phone, type, message)

    def test_registration_in_row(self):
        self.sub_test_registration_in_row(self.factory_user.get_phone('c', 1), 'c', 4)
        self.sub_test_registration_in_row(self.factory_user.get_phone('m', 1), 'm', 4)

    def sub_test_error_type(self, phone, type, message = '"error input fields"'):
        with self.subTest():
            response = self.registration(phone, type)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'error_status ' + message)
            self.assertIsNotNone(response.data, 'not 0 length ' + message)
            self.assertTrue(self.validater.validate_error(response.data, self.detail_registration_error_input_parameters))

    def test_registration_error_input_data(self):
        #error type
        self.sub_test_error_type(self.factory_user.get_phone('c', 0), 'q')
        self.sub_test_error_type(self.factory_user.get_phone('c', 1), 'cc')
        self.sub_test_error_type(self.factory_user.get_phone('c', 2), '1')
        self.sub_test_error_type(self.factory_user.get_phone('c', 3), '!=f')
        self.sub_test_error_type(self.factory_user.get_phone('c', 4), '.')
        self.sub_test_error_type(self.factory_user.get_phone('c', 5), 'с') #russian с

        #error phone
        self.sub_test_error_type('90000000010', 'с')
        self.sub_test_error_type('9', 'с')
        self.sub_test_error_type('900000000', 'с')
        self.sub_test_error_type('8000000000', 'с')
        self.sub_test_error_type('phonephone', 'с')
        self.sub_test_error_type('9honephone', 'с')