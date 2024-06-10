# Generated by Django 4.2.13 on 2024-06-09 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_user_marital_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('FR', 'Friend Request')], default='FR', max_length=2, verbose_name='Тип уведомления'),
        ),
    ]