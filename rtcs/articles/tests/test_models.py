from django.contrib.auth import get_user_model
from django.test import TestCase
from articles.models import Article, Comment


class TestArticleModel(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_article = Article.objects.create(title='Test title', content='Test content')
        return super().setUpClass()
    
    def test_article_title(cls):
        test_article = Article.objects.get(id=cls.test_article.id)
        
        cls.assertEqual(test_article.title, 'Test title')

    def test_article_content(cls):
        test_article = Article.objects.get(id=cls.test_article.id)

        cls.assertEqual(test_article.content, 'Test content')


class TestCommentModel(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_comment_author = get_user_model().objects.create(username='test_comment_author', password=123456)
        cls.test_article_for_comment = Article.objects.create(title='Test article for comment', content='Test content')
        cls.test_comment = Comment.objects.create(
            author=cls.test_comment_author,
            content='Test comment content',
            article=cls.test_article_for_comment
        )
        return super().setUpClass()
    
    def test_comment_author_credentials(cls):
        test_comment_object = Comment.objects.get(id=cls.test_comment.id)

        cls.assertEqual(test_comment_object.author.id, cls.test_comment_author.id)
    
    def test_comment_article(cls):
        test_comment_object = Comment.objects.get(id=cls.test_comment.id)

        cls.assertEqual(test_comment_object.article.id, cls.test_article_for_comment.id)

    def test_comment_content(cls):
        test_comment_object = Comment.objects.get(id=cls.test_comment.id)

        cls.assertEqual(test_comment_object.content, 'Test comment content')