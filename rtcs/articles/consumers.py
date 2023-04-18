import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class CommentConsumer(WebsocketConsumer):
        
    def connect(self):
        article_id = self.scope["url_route"]["kwargs"]["article_id"]
        self.room_group_name = f'article_{article_id}_comments'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        return super().receive(text_data, bytes_data)

    def send_article_comment(self, event): 
        message = event["message"]

        self.send(text_data=json.dumps({"message": message}))