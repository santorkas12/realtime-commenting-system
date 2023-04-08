

class RequestDataController:

    @classmethod
    def add_author_article_data_to_payload(cls, request, request_kwargs):
        author_id = request.user.id
        article_id = request_kwargs.get('article_id')

        request_data_update = {'author': author_id, 'article': article_id}

        return request_data_update

