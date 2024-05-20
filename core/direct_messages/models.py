from django.db import models
from account.models import User
# Create your models here.from django.db import models





class ChatModel(models.Model):
    """Сообщения чата"""
    sender = models.CharField(max_length=100, default=None)
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Cообщение:{self.message}  - {self.sender}: {self.thread_name}'
    
    class Meta:
        ordering = ('-timestamp',)
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
    
class ChatNotification(models.Model):
    """Оповещение"""
    chat = models.ForeignKey(to=ChatModel, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.user.username}'
    
    class Meta:
        ordering = ('is_seen',)
        verbose_name = 'Оповещение'
        verbose_name_plural = 'Оповещения'

