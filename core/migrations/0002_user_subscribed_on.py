# Generated by Django 2.0.1 on 2018-01-19 18:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='subscribed_on',
            field=models.ManyToManyField(blank=True, related_name='_user_subscribed_on_+', to=settings.AUTH_USER_MODEL),
        ),
    ]