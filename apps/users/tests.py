from rest_framework.test import APITestCase
from django.test import TestCase


from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from manuals.models import UserType, UserStatus
from users.models import PhoneCode


class AuthorizationTestCase(APITestCase):

    def setUp(self):
        UserType.objects.bulk_create([UserType(code="c", name="client"),
                                      UserType(code="m", name="master")])
        UserStatus.objects.bulk_create([UserStatus(code="rg", name="registered"),
                                        UserStatus(code="cf", name="confirmed"),
                                        UserStatus(code="bn", name="banned")])

    def test_client_auth(self):
        data = {
            'type_code': 'c',
            'phone': 9000000000
        }
        # registration
        response = self.client.post('/v1/users/registration/', data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        p = PhoneCode.objects.all()[0]
        data['code'] = p.code
        # confirmation
        response = self.client.post('/v1/users/confirmation/', data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('token', response.data.keys())

