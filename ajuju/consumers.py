from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from django.utils import timezone
from quiz.models import QuizAttempt

class ActiveWhizzerConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'active_whizzers'
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()
        self.send_active_whizzers_count()  # Send the initial count

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # Handle incoming messages if needed
        pass

    def send_active_whizzers_count(self):
        active_whizzers_count = QuizAttempt.objects.filter(
            start_time__gte=timezone.now() - timezone.timedelta(minutes=30),
            end_time__isnull=True
        ).values('whizzer').distinct().count()
        self.send(text_data=json.dumps({
            'type': 'active_whizzers_count',
            'count': active_whizzers_count
        }))

    def active_whizzers_count(self, event):
        # This method will handle the event sent from the channel layer
        self.send(text_data=json.dumps({
            'type': 'active_whizzers_count',
            'count': event['count']
        }))