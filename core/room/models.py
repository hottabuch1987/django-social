from django.db import models
from account.models import User


class Room(models.Model):
    name = models.CharField('Имя', max_length=255)
    slug = models.SlugField(unique=True)
    icon_html = models.TextField('HTML для иконки', blank=True, null=True) 
    
    def __str__(self):
        return f'{self.name}:{self.slug}'
    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='message', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='message', on_delete=models.CASCADE)
    content = models.TextField('Сообщение')
    date_added = models.DateTimeField('Дата сообщения', auto_now_add=True)

    def __str__(self):
        return f'Комната:{self.room}: Пользователь: {self.user} - дата:{self.date_added}'

    class Meta:
        ordering = ('date_added',)
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'