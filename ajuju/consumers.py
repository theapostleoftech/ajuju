import json

from channels.generic.websocket import AsyncWebsocketConsumer


class QuizConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.quiz_id = self.scope['url_route']['kwargs']['quiz_id']
        self.group_name = f'quiz_{self.quiz_id}'

        # Join quiz group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave quiz group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Send message to quiz group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'quiz_update',
                'data': data
            }
        )

    async def quiz_update(self, event):
        data = event['data']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(data))
