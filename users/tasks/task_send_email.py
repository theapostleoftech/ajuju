from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task(bind=True, max_retries=3)
def send_welcome_email(self, user_id: str) -> None:
    try:
        with transaction.atomic():
            user = get_user_model().objects.get(id=user_id)

            mail_subject = f"Welcome to Ajuju!"
            from_email = settings.DEFAULT_FROM_EMAIL
            context = {
                'user': user,
            }
            html_message = render_to_string('users/emails/welcome_email.html', context)
            plain_message = strip_tags(html_message)
            email = EmailMultiAlternatives(
                subject=mail_subject,
                body=plain_message,
                from_email=from_email,
                to=[user.email],
            )
            email.attach_alternative(html_message, 'text/html')
            email.send(fail_silently=False)
    except Exception as e:
        self.retry(exc=e, countdown=60)
