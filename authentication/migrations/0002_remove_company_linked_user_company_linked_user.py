# Generated by Django 5.0.6 on 2024-07-04 13:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='linked_user',
        ),
        migrations.AddField(
            model_name='company',
            name='linked_user',
            field=models.ManyToManyField(related_name='linked_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
