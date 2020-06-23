from django.test import TestCase

from django.core.management import call_command
from rest_framework import status

from tests.unit.users.tests import Server
from tests.unit.users.tests.FactoryEnvironment import FactoryEnvironment

import json

from tests.unit.users.tests.WrapperJsonValidation import WrapperJsonValidation

class test_users_get(TestCase):

    def setUp(self): #перед каждым методом
        call_command('flush', verbosity=0) #сбросить текущую бд
        #call_command("loaddata", 'fixtures.json', verbosity=0)
        call_command("loaddata", 'init_fixtures.json', verbosity=0)
        #self.factory_user = FactoryFixtures()
        self.validater = WrapperJsonValidation()
        self.factory_user = FactoryEnvironment()

    def validation(self, token):
        return Server.users(token)

    def sub_test_success_valid_client(self, token, type = None, user_status = None, message = '"valid client"'):
        with self.subTest():
            response = self.validation(token)
            self.assertEqual(response.status_code, status.HTTP_200_OK, 'error status ' + message)
            response_data = response.data
            self.assertIsNotNone(response_data, 'not 0 length ' + message)
            self.assertTrue(self.validater.validate_users_get_valid_client(response_data),
                            'json schema ' + message)

            response_data_loaded = None
            if type != None:
                response_data_loaded = json.loads(response_data)
                self.assertEqual(response_data_loaded['user']['type_code'], type)
            if user_status != None:
                self.assertEqual(response_data_loaded['user']['user_status'], user_status)

    def test_success_valid_client(self):
        phone1, token1 = self.factory_user.get_phone_with_valid_token('c',1, 'cf')
        self.sub_test_success_valid_client(token1, 'c', 'cf')

        phone2, token2 = self.factory_user.get_phone_with_valid_token('c',1, 'rg')
        self.sub_test_success_valid_client(token2, 'c', 'rg')

    def sub_test_success_valid_master(self, token, type = None, user_status = None, master_status = None, message = '"valid master"'):
        with self.subTest():
            response = self.validation(token)
            self.assertEqual(response.status_code, status.HTTP_200_OK, 'error status ' + message)
            response_data = response.data
            self.assertIsNotNone(response_data, '0 length data ' + message)
            self.assertTrue(self.validater.validate_users_get_valid_master(response_data),
                            'error answer ' + message)
            response_data_loaded = None
            if type != None:
                response_data_loaded = json.loads(response_data)
                self.assertEqual(response_data_loaded['user']['type_code'], type)
            if user_status != None:
                self.assertEqual(response_data_loaded['user']['user_status'], user_status)
            if master_status != None:
                self.assertEqual(response_data_loaded['user']['master']['master_status'], master_status)

    def test_success_valid_master(self):
        phone1, token1 = self.factory_user.get_phone_with_valid_token('m', 1, 'cf', 'vr')
        self.sub_test_success_valid_client(token1, 'm', 'cf', 'vr')

    def sub_test_invalid_token(self, token):
        with self.subTest():
            response = self.validation(token)
            self.assertEqual(response.status_code, status.HTTP_200_OK, 'error status ' + message)
            response_data = response.data
            self.assertIsNotNone(response_data, '0 length data ' + message)
            self.assertTrue(self.validater.validate_users_get_valid_master(response_data),
                            'error answer ' + message)
            response_data_loaded = None
            if type != None:
                response_data_loaded = json.loads(response_data)
                self.assertEqual(response_data_loaded['user']['type_code'], type)
            if user_status != None:
                self.assertEqual(response_data_loaded['user']['user_status'], user_status)
            if master_status != None:
                self.assertEqual(response_data_loaded['user']['master']['master_status'], master_status)

    def test_invalid_token(self):
