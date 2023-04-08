from rest_framework.routers import SimpleRouter
from .views import ArticleService, CommentService

router = SimpleRouter(trailing_slash=False)
router.register('', ArticleService)
router.register(r'(?P<article_id>\d+)/comments', CommentService)

urlpatterns = router.urls