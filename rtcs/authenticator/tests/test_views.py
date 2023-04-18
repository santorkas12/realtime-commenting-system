import json
from django.contrib.auth import get_user_model
from django.test import TestCase
from authenticator.views import LoginService
from rest_framework.test import APIClient

c = APIClient()

class TestLoginService(TestCase):

    @classmethod
    def setUpClass(cls):
        user = get_user_model()
        user_to_login = user.objects.create(username='test_login_service_user')
        user_to_login.set_password('123456')
        user_to_login.save()

        cls.valid_payload = {
            "username": "test_login_service_user",
            "password": "123456"
        }

        cls.invalid_payload = {
            "username": "username",
            "password": "123456"
        }

        return super().setUpClass()
    

    def test_login_response_valid(cls):
        login_response = c.post('/auth/login/', json.dumps(cls.valid_payload), content_type='application/json')

        cls.assertEqual(login_response.status_code, 200)
        cls.assertEqual(login_response.data, {'result': 'Success', 'message': 'Authenticated Successfully'})
        cls.assertIn('sessionid', login_response.cookies)


    def test_login_response_invalid(cls):
        response = cls.client.post('/auth/login/', data=json.dumps(cls.invalid_payload), content_type='application/json')

        cls.assertEqual(response.status_code, 400)
        cls.assertEqual(response.data, {'result': 'Fail', 'message': 'Invalid credentials'})
        cls.assertNotIn('sessionid', response.cookies)
