# Generated by Django 5.0.6 on 2024-07-04 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_remove_company_linked_user_company_linked_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='linked_user',
        ),
        migrations.DeleteModel(
            name='ActivationCompany',
        ),
        migrations.DeleteModel(
            name='Company',
        ),
    ]
