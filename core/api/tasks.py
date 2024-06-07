from celery import shared_task
from account.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


#filter users
@shared_task
def get_user_queryset_async(slug):
    queryset = User.objects.filter(slug=slug)
    return list(queryset.values())


#new message
@shared_task
def send_email_notification(subject, message, recipient_list):
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)


#periodic message
@shared_task
def send_periodic_message():
    subject = 'Вас давно не было в нашей системе!'
    message = 'Пора найти себе пару и завести новых друзей! '
    users = User.objects.all()
    for user in users:
        recipient_list = [user.email]
        print(recipient_list, 'send__mail')
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

