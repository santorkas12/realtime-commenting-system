from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=150, blank=False, null=False, verbose_name='Title')
    content = models.TextField(blank=False, null=False, verbose_name='Content')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Article'
        ordering = ['id']


class Comment(models.Model):
    author = models.ForeignKey(user, on_delete=models.CASCADE, related_name='comments',verbose_name='Author')
    content = models.TextField(blank=False, null=False, verbose_name='Content')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        verbose_name = 'Comment'
        ordering = ['id']
