from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import TestCase
from rest_framework.request import Request
from articles.controllers import RequestDataController

class TestRequestDataController(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        user_model = get_user_model()
        cls.request_user = user_model.objects.create(username='articles_test_controllers', password='123456')
        cls.test_request = Request(HttpRequest())
        cls.test_request.user = cls.request_user
        cls.kwargs_object = {'article_id': 1}
        return super().setUpClass()
    
    def test_add_author_article_data_to_payload(cls):
        initial_request_data = cls.test_request.data
        processes_request_data = RequestDataController.add_author_article_data_to_payload(cls.test_request, cls.kwargs_object)

        cls.assertFalse(initial_request_data)
        cls.assertIn('author', processes_request_data)
        cls.assertIn('article', processes_request_data)
        cls.assertEqual(processes_request_data.get('author'), cls.request_user.id)
        cls.assertEqual(processes_request_data.get('article'), cls.kwargs_object.get('article_id'))
