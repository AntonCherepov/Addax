from django.test import TestCase

# Create your tests here.

class URLTests(TestCase):

    def test_users(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
