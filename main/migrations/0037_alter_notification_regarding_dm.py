# Generated by Django 5.0.1 on 2024-04-23 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_notification_regarding_dm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='regarding_dm',
            field=models.CharField(default='', max_length=100),
        ),
    ]
