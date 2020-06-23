from django.test import TestCase

from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APIClient

from manuals.models import MasterType, City
from tests.unit.users.tests.FactoryEnvironment import FactoryEnvironment

import json
from jsonschema import validate

class test_logout_user(TestCase):
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
        call_command('flush', verbosity=0)
        call_command("loaddata", 'fixtures.json', verbosity=0)
        self.client = APIClient()
        self.url_logout = '/v1/users/logout/'
        self.factory_user = FactoryFixtures()

    def logout(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(self.url_logout)
        return response

    def sub_test_success_logout(self, token):
        with self.subTest():
            response = self.logout(token)