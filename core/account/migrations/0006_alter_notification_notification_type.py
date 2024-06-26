# Generated by Django 4.2.13 on 2024-06-09 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_notification_notification_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('FR', 'Добавить в друзья'), ('AFR', 'Принять заявку в друзья'), ('DFR', 'Отклонить заявку в друзья'), ('NM', 'Новое сообщение')], default='FR', max_length=10, verbose_name='Тип уведомления'),
        ),
    ]
