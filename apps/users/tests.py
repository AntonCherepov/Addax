from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK

from users.models import PhoneCode


class AuthorizationTestCase(APITestCase):

    def setUp(self):
        pass

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

