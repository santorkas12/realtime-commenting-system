from django.contrib import admin
from .models import Article, Comment

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'article', 'timestamp', 'author', 'content']

# Register your models here.
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
