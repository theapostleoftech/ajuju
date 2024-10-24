from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from quiz.models import QuizAttempt


@receiver(post_save, sender=QuizAttempt)
def send_active_whizzers_count_update(sender, instance, created, **kwargs):
    if created:
        # Send update when a new quiz attempt is started
        send_update()
    elif instance.end_time is not None:
        # Send update when a quiz attempt is finished
        send_update()


@receiver(pre_save, sender=QuizAttempt)
def send_active_whizzers_count_update_on_finish(sender, instance, **kwargs):
    if instance.end_time is not None and instance.pk:
        # Send update when a quiz attempt is finished (to handle zero count)
        send_update()


def send_update():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'active_whizzers',
        {
            'type': 'active_whizzers_count',
            'count': QuizAttempt.objects.filter(
                start_time__gte=timezone.now() - timezone.timedelta(minutes=30),
                end_time__isnull=True
            ).values('whizzer').distinct().count()
        }
    )
