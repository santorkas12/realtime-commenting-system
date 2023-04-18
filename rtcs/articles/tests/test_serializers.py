from django.contrib.auth import get_user_model
from django.test import TestCase
from articles.models import Article, Comment
from articles.serializers import ArticleSerializer, CommentSerializer


class TestArticleSerializer(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_article = Article.objects.create(title='Test title', content='Test content')
        cls.serializer = ArticleSerializer(cls.test_article)
        return super().setUpClass()
    
    def test_serializer_fields(cls):
        data = cls.serializer.data

        cls.assertEqual(data['id'], cls.test_article.id)
        cls.assertEqual(data['title'], cls.test_article.title)
        cls.assertEqual(data['content'], cls.test_article.content)

    
class TestCommentSerializer(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_article = Article.objects.create(title='Test title', content='Test content')
        cls.comment_author = get_user_model().objects.create(username='comment_author', password=123456)
        cls.comment = Comment.objects.create(
            author=cls.comment_author,
            content='test_content',
            article = cls.test_article 
        )

        cls.serializer = CommentSerializer(cls.comment)
        return super().setUpClass()
    
    def test_serializer_fields(cls):
        data = cls.serializer.data

        cls.assertEqual(data['id'], cls.comment.id)
        cls.assertEqual(data['author'], cls.comment_author.id)
        cls.assertEqual(data['content'], 'test_content')
        cls.assertEqual(data['article'], cls.test_article.id)
