# Generated by Django 4.2.13 on 2024-06-09 11:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('direct_messages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatnotification',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]