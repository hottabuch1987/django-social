from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, Group
from django.utils.timesince import timesince
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from datetime import date
from django.db.models import Q
import uuid
from django.urls import reverse
from django.utils.text import slugify
from datetime import datetime



class User(AbstractUser):
    """Пользователь"""
    GENDER_TYPES = (
        ("women", 'женщина'),
        ("men", 'мужчина'),
    )
    MARITAL_STATUS_CHOICES = (
        ('married', 'В браке'),
        ('single', 'Все сложно'),
        ('searching', 'В активном поиске'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    bio = models.TextField('Описание', max_length=500, blank=True)
    date_joined = models.DateTimeField("Дата регистрации", default=timezone.now)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    avatar = models.ImageField("Фото", upload_to='avatars', blank=True, null=True)
    gender = models.CharField("Пол", choices=GENDER_TYPES, default='men', max_length=10, blank=True, null=True)
    tel = models.CharField('Телефон', max_length=12, blank=True, null=True)
    friends = models.ManyToManyField('self', verbose_name="Друзья", blank=True)
    friends_count = models.IntegerField('Количество друзей', default=0)
    groups = models.ManyToManyField(Group, verbose_name='groups', blank=True)
    online_status = models.BooleanField(default=False, verbose_name="Online статус",)
    likes = models.ManyToManyField('self', related_name='likes', verbose_name="Лайки", blank=True)
    like_count = models.IntegerField(default=0, verbose_name="Количество лайков")
    slug = models.SlugField(unique=True)
    marital_status = models.CharField("Семейное положение", choices=MARITAL_STATUS_CHOICES, max_length=20, blank=True, null=True, default='searching')

    def __str__(self):
        return f'{self.username}: {self.first_name} - {self.email}'
    
  
    
    def get_avatar(self):
        if self.avatar:
            return 'http://195.133.32.53' + self.avatar.url
        else:
            return '/static/shop/images/avatar.png' + self.avatar.url

    def get_absolute_url(self):
        return reverse('account:detail-user', kwargs={'pk': self.id})
    
    @property
    def full_image_url(self):
        
        return self.avatar.url if self.avatar else ''
    
    def save(self, *args, **kwargs):
        if not self.slug:  # Генерация slug только если он не заполнен
            base_slug = slugify(self.username)  # Генерируем slug из поля username (в качестве примера)
            self.slug = base_slug
            count = 1
            while User.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = '{}-{}'.format(base_slug, count)  # Добавляем суффикс, если текущий slug уже занят
                count += 1
        is_new_user = not self.id
        if not is_new_user:
            initial_friends_count = self.friends_count
        super(User, self).save(*args, **kwargs)
        if not is_new_user:
            self.friends_count = self.friends.count()
            if initial_friends_count != self.friends_count:
                self.save(update_fields=['friends_count'])
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']


#images user
class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gallery', verbose_name="Галлерея фото")
    image = models.ImageField(upload_to='images/users/%Y/%m/%d', verbose_name="Изображение")

    class Meta:
        verbose_name = _(" Галлерея Изображений пользователя")
        verbose_name_plural = _("Галлерея Изображений пользователя")

    def get_image(self):
        if self.image:
            return 'http://195.133.32.53' + self.image.url
        else:
            return '/static/shop/images/avatar.png' + self.image.url

    def __str__(self):
        return f"Изибражение для {self.user.username}"
    
    @property
    def full_image_url(self):     
        return self.image.url if self.image else ''


#notification
class Notification(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_received')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_sent')
    message = models.TextField()
    timestamp = models.DateTimeField('Дата', auto_now_add=True)
    is_read = models.BooleanField('Прочитано', default=False)

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username}: {self.message}'
    
    class Meta:
        verbose_name = _(" Уведомления")
        verbose_name_plural = _("Уведомления")

class Forum(models.Model):
    """Форум"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name="Кто отправил")
    receiver = models.ManyToManyField(User, related_name='received_messages', verbose_name="Кому отправлено")
    content = RichTextUploadingField(verbose_name="Сообщение")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    message_file = models.FileField(upload_to="mails/%Y/%m/%d", verbose_name="Файл", blank=True, null=True)

    def __str__(self):
        return  f'{self.sender.username}  - {self.content} '
    
    class Meta:    
        verbose_name = 'Форум'
        verbose_name_plural = 'Форум'
        ordering = ['-timestamp']

phone = RegexValidator(regex=r'^\+?7?\d{11}$', message="Номер телефона должен быть в формате: '+7(999)999 99 99'.")

class Reviews(models.Model):
    """Обратная связь"""
    phone_number = models.CharField(max_length=12, validators=[phone], verbose_name='Номер телефона')
    text = models.TextField('Описание', max_length=250)
    def __str__(self):
        return f"Номер телефона: {self.phone_number}"

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратная связь"
        ordering = ['phone_number']

 