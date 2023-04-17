import base64
import json
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

c = APIClient()

class TestArticleService(TestCase):

    @classmethod
    def setUpClass(cls):
        user = get_user_model()
        article_service_request_user = user.objects.create(username='article_service_user', password='123456', is_superuser=True)
        c.force_login(article_service_request_user)

        cls.post_payload = {
            "title": "Article from test API",
            "content": "Article from test API - Content"
        }
        cls.post_response = c.post('/articles/', json.dumps(cls.post_payload), content_type='application/json')
        return super().setUpClass()
    
    def test_create_article(cls):
        post_response_data = cls.post_response.json()

        cls.assertEqual(cls.post_response.status_code, 201)
        cls.assertEqual(post_response_data.get('title'), cls.post_payload.get('title'))
        cls.assertEqual(post_response_data.get('content'), cls.post_payload.get('content'))

    def test_get_articles(cls):
        get_response = c.get('/articles/')
        get_response_data = get_response.json()

        cls.assertEqual(get_response.status_code, 200)
        cls.assertIsInstance(get_response_data, list)
        cls.assertEqual(len(get_response_data), 1)

    def test_retrieve_article(cls):
        retrieve_response = c.get('/articles/1')
        retrieve_response_data = retrieve_response.json()

        cls.assertEqual(retrieve_response.status_code, 200)
        cls.assertIsInstance(retrieve_response_data, dict)
        cls.assertEqual(retrieve_response_data.get('title'), cls.post_payload.get('title'))

    def test_put_article(cls):
        put_payload = {
            "title": "Article from test API - PUT Modified",
            "content": "Article from test API - Content - PUT Modified"
        }
        put_response = c.put('/articles/1', json.dumps(put_payload), content_type='application/json')
        put_response_data = put_response.json()

        cls.assertEqual(put_response.status_code, 200)
        cls.assertEqual(put_response_data.get('title'), put_payload.get('title'))
        cls.assertEqual(put_response_data.get('content'), put_payload.get('content'))
        
    def test_delete_article(cls):
        delete_response = c.delete('/articles/1')

        cls.assertEqual(delete_response.status_code, 204)

        get_response = c.get('/articles/')
        cls.assertEqual(get_response.status_code, 200)
        cls.assertFalse(get_response.json())
        

class TestCommentService(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        user = get_user_model()
        cls.comment_service_request_user = user.objects.create(username='comment_service', password='123456', is_superuser=True)
        c.force_login(cls.comment_service_request_user)

        
        create_article_payload = {
            "title": "Article from test API",
            "content": "Article from test API - Content"
        }
        c.post('/articles/', json.dumps(create_article_payload), content_type='application/json')

        cls.post_payload = {
            "content": "This is the 1st comment on article 1 in test db. It only needs a 'content' payload key. All other attributes are handled by the server!"
        }
        cls.post_response = c.post('/articles/1/comments', json.dumps(cls.post_payload), content_type='application/json')
        return super().setUpClass()
    
    def test_create_comment(cls):
        post_response_data = cls.post_response.json()

        cls.assertEqual(cls.post_response.status_code, 201)
        cls.assertEqual(post_response_data.get('article'), 1)
        cls.assertEqual(post_response_data.get('content'), cls.post_payload.get('content'))
        cls.assertEqual(post_response_data.get('author'), cls.comment_service_request_user.id)

    def test_get_article_comments(cls):
        get_response = c.get('/articles/1/comments')
        get_response_data = get_response.json()

        cls.assertEqual(get_response.status_code, 200)
        cls.assertIsInstance(get_response_data, list)
        cls.assertEqual(len(get_response_data), 1)

    def test_put_article_comment(cls):
        put_payload = {
            "content": "This is the 1st comment on article 1 in test db. Its content has been modified by a put request."
        }
        put_response = c.put('/articles/1/comments/1', json.dumps(put_payload), content_type='application/json')
        put_response_data = put_response.json()

        cls.assertEqual(put_response.status_code, 200)
        cls.assertEqual(put_response_data.get('content'), put_payload.get('content'))

    def test_delete_article_comment(cls):
        delete_response = c.delete('/articles/1/comments/1')

        cls.assertEqual(delete_response.status_code, 204)
        get_response = c.get('/articles/1/comments/1')
        cls.assertEqual(get_response.status_code, 404)