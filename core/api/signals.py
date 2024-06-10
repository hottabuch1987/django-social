from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from direct_messages.models import ChatNotification
from .tasks import send_email_notification


@receiver(post_save, sender=ChatNotification)
def send_email_on_chat_notification_creation(sender, instance, created, **kwargs):
    if created:
        subject = 'У вас новое сообщение в чате!'
        message = f'Привет {instance.user.username}, у вас новое сообщение!'
        recipient_list = [instance.user.email]
        print(recipient_list, message, subject, 'send__mail')
        # send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

        send_email_notification.delay(subject, message, recipient_list)
