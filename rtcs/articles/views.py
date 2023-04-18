from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
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
        new_comment_response = super().create(request, *args, **kwargs)
        self._send_update_over_websocket(new_comment_response.data)

        return new_comment_response
    
    def update(self, request, *args, **kwargs):
        request.data.update(RequestDataController.add_author_article_data_to_payload(request, kwargs))
        return super().update(request, *args, **kwargs)
    
    def _send_update_over_websocket(self, new_comment):
        article_id = new_comment.get('article')
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'article_{article_id}_comments',
            {
                "type": "send_article_comment",
                "message": new_comment
            }
        )
