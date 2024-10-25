from datetime import timedelta

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from quiz.models import QuizAttempt


@receiver(post_save, sender=QuizAttempt)
def send_active_whizzers_update(sender, instance, created, **kwargs):
    if created or (instance.end_time is not None and instance.end_time != instance.__class__.objects.get(
            pk=instance.pk).end_time):
        # Send update when a new quiz attempt is started or finished
        send_update()


@receiver(pre_save, sender=QuizAttempt)
def send_active_whizzers_update_on_finish(sender, instance, **kwargs):
    if instance.end_time is not None and instance.pk:
        previous_instance = sender.objects.get(pk=instance.pk)
        if previous_instance.end_time is None:  # Only send update if end_time is changing from None to a value
            send_update()


import logging

logger = logging.getLogger(__name__)


def send_update():
    channel_layer = get_channel_layer()
    active_whizzers = QuizAttempt.objects.filter(
        start_time__gte=timezone.now() - timedelta(minutes=0),
        end_time__isnull=True
    ).select_related('whizzer', 'quiz')

    whizzer_details = []
    for attempt in active_whizzers:
        time_left = (attempt.start_time + timedelta(minutes=attempt.quiz.time_limit) - timezone.now()).total_seconds()
        whizzer_details.append({
            'username': attempt.whizzer.user.username,
            'quiz_title': attempt.quiz.title,
            'time_left': max(0, int(time_left))
        })

    logger.info(f"Sending update: {whizzer_details}")

    async_to_sync(channel_layer.group_send)(
        'active_whizzers',
        {
            'type': 'active_whizzers_details',
            'whizzers': whizzer_details,
            'count': len(whizzer_details)
        }
    )
