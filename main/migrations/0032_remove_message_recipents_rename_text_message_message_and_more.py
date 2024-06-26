# Generated by Django 5.0.1 on 2024-04-16 18:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_merge_20240409_1424'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='recipents',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='text',
            new_name='message',
        ),
        migrations.RemoveField(
            model_name='message',
            name='creator',
        ),
        migrations.AddField(
            model_name='message',
            name='dmid',
            field=models.CharField(default=None, max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Recipient_Group',
        ),
    ]
