from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Forum, User

@shared_task
def send_registration_email(username, email):
    subject = 'Добро пожаловать в нашу систему!'
    message = render_to_string('email/mail.html', {
        'username': username,
        'email': email,

    })
    send_mail(subject, None, 'varvar1987a@mail.ru', [email], [username], html_message=message)



@shared_task
def send_forum_message(message_id):
    message = Forum.objects.get(id=message_id)



