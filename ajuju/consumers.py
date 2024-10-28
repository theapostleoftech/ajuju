import json
import logging
from datetime import timedelta

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone

from quiz.models import QuizAttempt

logger = logging.getLogger(__name__)


class ActiveWhizzerConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'active_whizzers'
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()
        logger.info("WebSocket connection accepted. Sending initial active whizzers details.")
        self.send_active_whizzers_details()  # Send initial details of active whizzers

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        logger.info("WebSocket connection closed.")

    def receive(self, text_data):
        # Handle incoming messages if needed
        pass

    def send_active_whizzers_details(self):
        active_whizzers = QuizAttempt.objects.filter(
            start_time__gte=timezone.now() - timedelta(minutes=30),
            end_time__isnull=True
        ).select_related('whizzer', 'quiz')

        whizzer_details = []
        for attempt in active_whizzers:
            time_left = (attempt.start_time + timedelta(
                minutes=attempt.quiz.time_limit) - timezone.now()).total_seconds()
            whizzer_details.append({
                'username': attempt.whizzer.user.username,
                'quiz_title': attempt.quiz.title,
                'time_left': max(0, int(time_left))  # Ensure time left is not negative
            })

        self.send(text_data=json.dumps({
            'type': 'active_whizzers_details',
            'whizzers': whizzer_details,
            'count': len(whizzer_details)
        }))

    def active_whizzers_count(self, event):
        # This method will handle the event sent from the channel layer
        self.send(text_data=json.dumps({
            'type': 'active_whizzers_count',
            'count': event['count']
        }))

    def active_whizzers_details(self, event):
        # This method will handle the event sent from the channel layer for whizzer details
        self.send(text_data=json.dumps({
            'type': 'active_whizzers_details',
            'whizzers': event['whizzers'],
            'count': event['count']
        }))
