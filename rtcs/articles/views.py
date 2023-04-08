from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet
from .controllers import RequestDataController
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer


# Create your views here.
class ArticleService(ModelViewSet):
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    serializer_class = ArticleSerializer


class CommentService(ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return self.queryset.filter(article_id=self.kwargs.get('article_id'))

    def create(self, request, *args, **kwargs):
        request.data.update(RequestDataController.add_author_article_data_to_payload(request, kwargs))
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        request.data.update(RequestDataController.add_author_article_data_to_payload(request, kwargs))
        return super().update(request, *args, **kwargs)