# Generated by Django 5.0.1 on 2024-02-28 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_rename_recipent_group_recipient_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='seen',
        ),
        migrations.AddField(
            model_name='recipient_group',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
